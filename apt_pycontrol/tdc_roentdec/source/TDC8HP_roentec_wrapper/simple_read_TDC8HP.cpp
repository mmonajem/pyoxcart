//////////////////////////////////////////////////////////////////////////////////////////
//
//	written by Achim Czasch (RoentDek Handels Gmbh)
//
//////////////////////////////////////////////////////////////////////////////////////////

#include <queue>

#include "tdcmanager.h"
#include "afx.h" // only needed for the CStrings in this example
#include "conio.h"

#include "LMF_IO.h"
#define NUM_CHANNELS (80)
#define NUM_IONS (32)


#define READ_BUFFER_SIZE (50000)
// this size can be set to other values

#ifdef WIN64
	#pragma comment(lib,"hptdc_driver_3.5.2_x64.lib")
#else
	#pragma comment(lib,"hptdc_driver_3.5.2_x86.lib")
#endif


__int32 trigger_channel;



bool PCIGetTDC_25psGroupMode_TDC8HP(TDCManager * manager, unsigned __int32  CNT[], __int32  TDC[][10], unsigned __int32 Max_channels, unsigned __int32 Max_hits, unsigned __int64 &ui64_HPTDC_AbsoluteTimeStamp);


class Wrraper_tdc
{
public:
	Wrraper_tdc();
	double* reader_tdc();
	int run_tdc();

private:
	queue<double> x;
	queue<double> y;
	queue<double> tof;
	queue<double> time_stamp;

};

Wrraper_tdc::Wrraper_tdc()
{

};

double* Wrraper_tdc::reader_tdc()
{


	//printf("Reading the queues\n");
	queue<double> gx = x;
	x = {};
	queue<double> gy = y;
	y = {};
	queue<double> gtof = tof;
	tof = {};
	queue<double> gtime_stamp = time_stamp;
	time_stamp = {};

	double* array_tem = new double[4*10000];
	double array[4][10000];

	int size = gx.size();

	if (size == gy.size() && size == gtof.size() && size == gtime_stamp.size()) {
		int index = 0;
		while (!gx.empty()) {
			array[0][index] = gx.front();
			gx.pop();
			array[1][index] = gy.front();
			gy.pop();
			array[2][index] = gtof.front();
			gtof.pop();
			array[3][index] = gtime_stamp.front();
			gtime_stamp.pop();
			index = index + 1;
		}
	}

	for (int i = 0; i < 8; ++i) {
		for (int j = 0; j < 1024; ++j) {
			// mapping 1D array to 2D array
			array_tem[i * 10000 + j] = array[i][j];
		}
	}
	return array_tem;
};

int Wrraper_tdc::run_tdc()
{
	trigger_channel = 8 - 1; // 1st TDC channel has index 0

	printf("hit q to quit.\n");

	unsigned __int64 ui64_HPTDC_AbsoluteTimeStamp = 0;

	//  --------------------------------------------------------
	//	read Header information of template LMF-file (ignore this part)
	LMF_IO* LMF = new LMF_IO(NUM_CHANNELS, NUM_IONS);
	char template_name[270];
	sprintf(template_name, "%s", "apt");
	while (strlen(template_name) > 0) {
		if (template_name[strlen(template_name) - 1] == '\\' || template_name[strlen(template_name) - 1] == '/') {
			break;
		}
		template_name[strlen(template_name) - 1] = 0;
	}


	sprintf(template_name + strlen(template_name), "%s", "CoboldPC2011R5-2_Header-Tempalte_1TDC8HP.lmf");

	if (!LMF->OpenInputLMF(template_name)) {
		printf("error: could not open the template file\n%s\n", template_name);
		printf("It must be in the same folder as the exe.\n");
		return false;
	}
	LMF->CloseInputLMF();
	//  --------------------------------------------------------


	// now configure the TDC:
	TDCManager* manager = new TDCManager(0x1A13, 0x0001);
	if (!manager) return 0;

	manager->Init();

	TDCInfo myTDC;
	myTDC = manager->getTDCInfo(0);
	int Firmware = (myTDC.version & 0xff);
	if (Firmware < 6) printf("Please update the firmware of the TDC.\n");
	double tdc_binsize = myTDC.resolution * 1.e9;
	double timestamp_binsize = tdc_binsize;

	// note: please do not confuse binsize with resolution. The real (internal) binsize of each channel is 25 ps.
	//       Therefore the resolution of a measured time (e.g. channel 1 vs. trigger channel) is sqrt(2)*25ps = 34ps FWHM = 14.5 ps RMS. 

	// now reconfigure the TDC (necessary after all parameters are set):
	manager->Reconfigure();

	LMF->TDC8HP.GroupRangeEnd_p70 = atof(manager->GetParameter("GroupRangeEnd"));
	LMF->TDC8HP.GroupRangeStart_p69 = atof(manager->GetParameter("GroupRangeStart"));
	LMF->TDC8HP.TriggerDeadTime_p68 = atof(manager->GetParameter("Triggerdeadtime"));
	LMF->TDC8HP.TriggerChannel_p64 = atoi(manager->GetParameter("triggerchannel"));

	LMF->tdcresolution_output = myTDC.resolution * 1e9;

	//	Open and prepare output file
	LMF->number_of_channels_output = 8;
	LMF->max_number_of_hits_output = 10;
	LMF->frequency = 1.;
	LMF->OpenOutputLMF("output.lmf");

	//  now read events from TDC
	unsigned __int32	CNT[8];
	__int32				TDC_data[8][10];

	manager->Start();
	__int64 recorded_triggers = 0;

	__int64 last_tick_ms = GetTickCount64();

	// The calibration factors 
	__int64 fu = 1;
	__int64 fv = 1;


	while (true) {
		++recorded_triggers;
		memset(TDC_data, 0, sizeof(TDC_data));	// clear TDC_data[] array

		bool group_is_complete = false;
		while (!group_is_complete) {
			group_is_complete = PCIGetTDC_25psGroupMode_TDC8HP(manager, CNT, TDC_data, 8, 10, ui64_HPTDC_AbsoluteTimeStamp);
			if (!group_is_complete) {
				Sleep(1);
				if (_kbhit())
					break;
			}
		}

		// Calculate the X, Y, Time of Flight , and Time_stamp
		double X = (TDC_data[1][0] - TDC_data[0][0]) * fu; 
		double Y = (X - 2. * (TDC_data[3][0] - TDC_data[2][0]) * fv) / sqrt(3);
		double TOF = (TDC_data[0][0] + TDC_data[1][0]) / 2;
		double TIME_STAMP = ui64_HPTDC_AbsoluteTimeStamp;

		// push calculated values to the qeues
		x.push(X);
		y.push(Y);
		tof.push(TOF);
		time_stamp.push(TIME_STAMP);

		LMF->WriteTDCData(ui64_HPTDC_AbsoluteTimeStamp, CNT, &TDC_data[0][0]);



		if (recorded_triggers % 1000) {
			__int64 tt = GetTickCount64();
			if (tt - last_tick_ms > 500) {
				if (_kbhit()) {
					char c = _getch();
					if (c == 'q') break;
					printf("hit q to exit.\n");
					while (_kbhit()) _getch();
				}
				last_tick_ms = tt;
			}
		}
	}


	// stop TDC
	printf("stopping the TDC.\n");
	manager->Stop();
	manager->ClearBuffer();

	manager->CleanUp(); // cleanup is necessary before delete.
	delete (TDCManager*)manager;



	if (LMF) {
		LMF->CloseOutputLMF();
		delete LMF;
	}
	return 0;
}

// Define C functions for the C++ class - as ctypes can only talk to C...
extern "C"
{
	__declspec(dllexport) Wrraper_tdc* Warraper_tdc_new() { return new Wrraper_tdc(); }
	__declspec(dllexport) double* reader(Wrraper_tdc* Wrraper_tdc) { return Wrraper_tdc->reader_tdc(); }
	__declspec(dllexport) int run_tdc(Wrraper_tdc* Wrraper_tdc) { return Wrraper_tdc->run_tdc(); }
}


//////////////////////////////////////////////////////////////////////////////////////////
int main(int argc, char* argv[], char* envp[])
//////////////////////////////////////////////////////////////////////////////////////////
{
	
	return 0;
}





/////////////////////////////////////////////////////////////////// 
// 25ps GroupMode:
// In this mode the grouping is done inside the TDC driver
///////////////////////////////////////////////////////////////////
bool PCIGetTDC_25psGroupMode_TDC8HP(TDCManager * manager, unsigned __int32 CNT[], __int32 TDC[][10], unsigned __int32 Max_channels, unsigned __int32 Max_hits, unsigned __int64 &ui64_HPTDC_AbsoluteTimeStamp)
{
	HIT buffer[READ_BUFFER_SIZE];

	memset(CNT,0,sizeof(__int32)*Max_channels);

	static unsigned __int32 ulRollOver = 0;
	static unsigned __int32 ulAbsoluteTimeStamp = 0;
	static unsigned __int64	ui64_OldTimeStamp = 0;
	
	if (!ui64_HPTDC_AbsoluteTimeStamp) {
		ulRollOver = 0;
		ulAbsoluteTimeStamp = 0;
		ui64_OldTimeStamp = 0;
	}

	//------------------------------------------
	// Read one Event, count = number of hits
	//------------------------------------------
	unsigned __int32 count = manager->Read(buffer, READ_BUFFER_SIZE);
	if(!count) return false;
	//------------------------------------------

	bool bOKFlag = false;
	// now process the data
	for(unsigned __int32 i = 0; i < count ; ++i)
	{
		unsigned __int32 uldata_word = buffer[i];

		if( (uldata_word&0xC0000000) > 0x40000000)		// valid data only if rising or falling transition
		{
			long lTDCData = (uldata_word&0x00FFFFFF);
			if(lTDCData & 0x00800000) lTDCData |= 0xff000000;	// detect 24 bit signed flag:  if detected extend negative value to 32 bit

			unsigned char ucTDCChannel = (unsigned char)((uldata_word&0x3F000000)>>24);	// extract channel information
			
			if(ucTDCChannel < Max_channels)	// if detected channel fits into TDC array ...
			{
				// increase Hit Counter;
				++CNT[ucTDCChannel];

				// test for oversized Hits
				if(CNT[ucTDCChannel] > Max_hits) {
					--CNT[ucTDCChannel];
				} else {
					// if Hit # ok then store it
					TDC[ucTDCChannel][CNT[ucTDCChannel]-1] = lTDCData;
					bOKFlag = true;
				}
			}
		} else {
			if (uldata_word >> 24 == 0x10) {
				ulRollOver = uldata_word & 0xffffff; // RollOverWord detected ?
			}
			if (!(uldata_word & 0xf0000000)) ulAbsoluteTimeStamp = uldata_word & 0xffffff; // GroupWord detected
		}
	}	

	if (count) {
		unsigned __int64 ui64_TimeStamp_temp = ulRollOver * 0x1000000ull + ulAbsoluteTimeStamp;

		// handle 48 bit rollovers:
		ui64_HPTDC_AbsoluteTimeStamp += ui64_TimeStamp_temp - ui64_OldTimeStamp;
		if (ui64_TimeStamp_temp < ui64_OldTimeStamp) {
			ui64_HPTDC_AbsoluteTimeStamp += 0x1000000000000ull; 
		}

		ui64_OldTimeStamp = ui64_TimeStamp_temp;
	}

	return bOKFlag;
}


