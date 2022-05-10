//////////////////////////////////////////////////////////////////////////////////////////
//
//	written by Achim Czasch (RoentDek Handels Gmbh)
//  Modified by Mehrpad Monajem (mehrpad.monajem@fau.de)
//
//////////////////////////////////////////////////////////////////////////////////////////

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
	int init_tdc();
	int run_tdc();
	int stop_tdc();
	float* get_data_tdc();


private:

	// now configure the TDC:
	TDCManager* manager = new TDCManager(0x1A13, 0x0001);
	LMF_IO* LMF = new LMF_IO(NUM_CHANNELS, NUM_IONS);

};

Wrraper_tdc::Wrraper_tdc()
{

};



int Wrraper_tdc::init_tdc()
{

	//  --------------------------------------------------------
	//	read Header information of template LMF-file (ignore this part)
	char template_name[270] = "simple_read_TDC8HP_x64.exp";


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
		return 1;
	}
	LMF->CloseInputLMF();
	//  --------------------------------------------------------

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

	return 0;
};

int Wrraper_tdc::run_tdc()
{
	manager->Start();
	return 0;
};

int Wrraper_tdc::stop_tdc()
{
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
};


float* Wrraper_tdc::get_data_tdc()
{
	trigger_channel = 8 - 1; // 1st TDC channel has index 0

	unsigned __int64 ui64_HPTDC_AbsoluteTimeStamp = 0;


	// note: please do not confuse binsize with resolution. The real (internal) binsize of each channel is 25 ps.
	//       Therefore the resolution of a measured time (e.g. channel 1 vs. trigger channel) is sqrt(2)*25ps = 34ps FWHM = 14.5 ps RMS. 


	//  now read events from TDC
	unsigned __int32	CNT[8];
	__int32				TDC_data[8][10];

	
	__int64 recorded_triggers = 0;

	//__int64 last_tick_ms = GetTickCount64();


	++recorded_triggers;
	memset(TDC_data, 0, sizeof(TDC_data));	// clear TDC_data[] array

	//manager->Continue();

	bool group_is_complete = false;
	while (!group_is_complete) {
		group_is_complete = PCIGetTDC_25psGroupMode_TDC8HP(manager, CNT, TDC_data, 8, 10, ui64_HPTDC_AbsoluteTimeStamp);
		if (!group_is_complete) {
			Sleep(1);
		}
	}

	//manager->Pause();

	// It is possible to calculate the X, Y, ToF, Time_stamp and send them, instead of the TDC data
	// Calculate the X, Y, Time of Flight, and Time_stamp
	//float fu = 1;
	//float fv = 1;
	//float X = (TDC_data[1][0] - TDC_data[0][0]) * fu; 
	//float Y = (X - 2. * (TDC_data[3][0] - TDC_data[2][0]) * fv) / sqrt(3);
	//float TOF = abs(TDC_data[7][0] - TDC_data[6][0]);


	LMF->WriteTDCData(ui64_HPTDC_AbsoluteTimeStamp, CNT, &TDC_data[0][0]);

	float* array_tem = new float[9];

	for (int i = 0; i < 10; ++i) {
		if (i < 8) {
			array_tem[i] = static_cast<float>(TDC_data[i][0]);
		}
		else {
			array_tem[i] = ui64_HPTDC_AbsoluteTimeStamp;
		}
		
	}

	return array_tem;
}

/*
// Version 2 of get_data_tdc with buffering the data to reduce returning number to python
// It buffers 1000 event and then return the result to Python wrraper.
float* Wrraper_tdc::get_data_tdc()
{
	trigger_channel = 8 - 1; // 1st TDC channel has index 0

	unsigned __int64 ui64_HPTDC_AbsoluteTimeStamp = 0;


	// note: please do not confuse binsize with resolution. The real (internal) binsize of each channel is 25 ps.
	//       Therefore the resolution of a measured time (e.g. channel 1 vs. trigger channel) is sqrt(2)*25ps = 34ps FWHM = 14.5 ps RMS. 


	//  now read events from TDC
	unsigned __int32	CNT[8];
	__int32				TDC_data[8][10];


	__int64 recorded_triggers = 0;

	//__int64 last_tick_ms = GetTickCount64();

	float* array_tem = new float[9*1000];

	while (true) {

		memset(TDC_data, 0, sizeof(TDC_data));	// clear TDC_data[] array

		//manager->Continue();

		bool group_is_complete = false;
		while (!group_is_complete) {
			group_is_complete = PCIGetTDC_25psGroupMode_TDC8HP(manager, CNT, TDC_data, 8, 10, ui64_HPTDC_AbsoluteTimeStamp);
			if (!group_is_complete) {
				Sleep(1);
			}
		}

		//manager->Pause();

		// It is possible to calculate the X, Y, ToF, Time_stamp and send them, instead of the TDC data
		// Calculate the X, Y, Time of Flight, and Time_stamp
		//float fu = 1;
		//float fv = 1;
		//float X = (TDC_data[1][0] - TDC_data[0][0]) * fu; 
		//float Y = (X - 2. * (TDC_data[3][0] - TDC_data[2][0]) * fv) / sqrt(3);
		//float TOF = abs(TDC_data[7][0] - TDC_data[6][0]);


		LMF->WriteTDCData(ui64_HPTDC_AbsoluteTimeStamp, CNT, &TDC_data[0][0]);

		float* array_tem = new float[9];

		for (int i = 0; i < 10; ++i) {
			if (i < 8) {
				array_tem[i] = static_cast<float>(TDC_data[i + 9 * recorded_triggers][0]);
			}
			else {
				array_tem[i] = ui64_HPTDC_AbsoluteTimeStamp;
			}

		}

		if (recorded_triggers % 1000) {
			break;
		}
	}
	++recorded_triggers;
	return array_tem;
}
*/

// Define C functions for the C++ class - as ctypes can only talk to C...
extern "C"
{
	__declspec(dllexport) Wrraper_tdc* Warraper_tdc_new() { return new Wrraper_tdc(); }
	__declspec(dllexport) int init_tdc(Wrraper_tdc* Wrraper_tdc) { return Wrraper_tdc->init_tdc(); }
	__declspec(dllexport) int run_tdc(Wrraper_tdc* Wrraper_tdc) { return Wrraper_tdc->run_tdc(); }
	__declspec(dllexport) int stop_tdc(Wrraper_tdc* Wrraper_tdc) { return Wrraper_tdc->stop_tdc(); }
	__declspec(dllexport) float* get_data_tdc(Wrraper_tdc* Wrraper_tdc) { return Wrraper_tdc->get_data_tdc(); }
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


