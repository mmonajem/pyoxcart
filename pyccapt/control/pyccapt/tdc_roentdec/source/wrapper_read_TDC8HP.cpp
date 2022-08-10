//////////////////////////////////////////////////////////////////////////////////////////
//
//	written by Achim Czasch (RoentDek Handels Gmbh)
//
//////////////////////////////////////////////////////////////////////////////////////////


#include <chrono>
#include <iostream>
using namespace std;
using namespace std::chrono;

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





bool PCIGetTDC_25psGroupMode_TDC8HP(TDCManager * manager, unsigned __int32  CNT[], __int32  TDC[][10], unsigned __int32 Max_channels, unsigned __int32 Max_hits, unsigned __int64 &ui64_HPTDC_AbsoluteTimeStamp);


class Wrraper_tdc
{
public:
	Wrraper_tdc(int, int);
	int init_tdc();
	int run_tdc();
	int stop_tdc();
	double* get_data_tdc();
	double* get_data_tdc_buf();


private:

	// now configure the TDC:
	TDCManager* manager = new TDCManager(0x1A13, 0x0001);
	LMF_IO* LMF = new LMF_IO(NUM_CHANNELS, NUM_IONS);

	int buffer_size;
	int time_out_micro;

	__int32 trigger_channel;


	unsigned __int64 ui64_HPTDC_AbsoluteTimeStamp;
	// note: please do not confuse binsize with resolution. The real (internal) binsize of each channel is 25 ps.
	//       Therefore the resolution of a measured time (e.g. channel 1 vs. trigger channel) is sqrt(2)*25ps = 34ps FWHM = 14.5 ps RMS.

	__int64 recorded_triggers = 0;
	__int64 last_tick_ms = GetTickCount64();



	//  now read events from TDC
	unsigned __int32	CNT[8];
	__int32				TDC_data[8][10];

	double fu;
	double fv;
	double fw;
	double w_offset;

	double u;
	double v;
	double w;

	double X;
	double Y;
	double TOF;

	double* array_tem;

	double tdc_binsize;

};

Wrraper_tdc::Wrraper_tdc(int buf_size, int time_out)
{
	buffer_size = buf_size;
	time_out_micro = time_out * 1000; // convert it from milisecond to microsecond
	trigger_channel = 8 - 1; // 1st TDC channel has index 0
	ui64_HPTDC_AbsoluteTimeStamp = 0;

	fu = 0.890000; // Time to mm calibration factor for u (mm/ns)
	fv = 0.917000; //Time to mm calibration factor for v (mm/ns)
	fw = 0.887000; //Time to mm calibration factor for w (mm/ns)
	w_offset = -1.175000; //Offset for w layer (units: nanoseconds)

	u = 0;
	v = 0;
	w = 0;

	X = 0;
	Y = 0;
	TOF = 0;

	array_tem = new double[(12 * buffer_size) + 1]; //+1 for putting the siye of array

};



int Wrraper_tdc::init_tdc()
{

	//  --------------------------------------------------------
	//	read Header information of template LMF-file (ignore this part)
	char template_name[270] = "simple_read_TDC8HP";


	while (strlen(template_name) > 0) {
		if (template_name[strlen(template_name) - 1] == '\\' || template_name[strlen(template_name) - 1] == '/') {
			break;
		}
		template_name[strlen(template_name) - 1] = 0;
	}

	sprintf(template_name + strlen(template_name), "%s", "CoboldPC2011R5-2_Header-Template_1TDC8HP.lmf");

	if (!LMF->OpenInputLMF(template_name)) {
		printf("error: could not open the template file\n%s\n", template_name);
		printf("It must be in the same folder as the exe.\n");
		return 1;
	}
	LMF->CloseInputLMF();
	//  --------------------------------------------------------

	if (!manager) return -1;

	manager->Init();

	TDCInfo myTDC;
	myTDC = manager->getTDCInfo(0);
	int Firmware = (myTDC.version & 0xff);
	if (Firmware < 6) printf("Please update the firmware of the TDC.\n");


	tdc_binsize = myTDC.resolution * 1.e9;
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


double* Wrraper_tdc::get_data_tdc()
{

	memset(TDC_data, 0, sizeof(TDC_data));	// clear TDC_data[] array
	memset(array_tem, 0, sizeof(array_tem));

	//manager->Continue();

	bool group_is_complete = false;
	while (!group_is_complete) {
		group_is_complete = PCIGetTDC_25psGroupMode_TDC8HP(manager, CNT, TDC_data, 8, 10, ui64_HPTDC_AbsoluteTimeStamp);
		if (!group_is_complete) {
			Sleep(1);
		}
	}

	//manager->Pause();

	// Calculate the X, Y, Time of Flight, number of written events in lmf file , and Time_stamp
	//static_cast<float>(
	u = (1 / 2) * ((TDC_data[0][0] * tdc_binsize) - (TDC_data[1][0] * tdc_binsize)) * fu;
	v = (1 / 2) * ((TDC_data[2][0] * tdc_binsize) - (TDC_data[3][0] * tdc_binsize)) * fv;
	w = (1 / 2) * (((TDC_data[4][0] * tdc_binsize) - (TDC_data[5][0] * tdc_binsize)) + w_offset) * fw;

	X = u;
	Y = (u - (2 * v)) / sqrt(3);
	TOF = (TDC_data[7][0] * tdc_binsize) - (TDC_data[6][0] * tdc_binsize);


	LMF->WriteTDCData(ui64_HPTDC_AbsoluteTimeStamp, CNT, &TDC_data[0][0]);

	array_tem[0] = 1;
	for (int i = 0; i < 12; ++i) {
		if (i < 8) {
			array_tem[i + 1] = TDC_data[i][0];
		}
		else if (i == 8) {
			array_tem[i + 1] = X;
		}
		else if (i == 9) {
			array_tem[i + 1] = Y;
		}
		else if (i == 10) {
			array_tem[i + 1] = TOF;
		}
		else {
			array_tem[i + 1] = static_cast<double>(ui64_HPTDC_AbsoluteTimeStamp);
		}
		
	}

	return array_tem;
}


// Version 2 of get_data_tdc with buffering the data to reduce returning number to python
// It buffers events and then return the result to Python wrraper.
double* Wrraper_tdc::get_data_tdc_buf()
{
	memset(array_tem, 0, sizeof(array_tem));

	auto start = high_resolution_clock::now();

	while (true) {

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
		//cout << TDC_data[4][0] << endl;
		LMF->WriteTDCData(ui64_HPTDC_AbsoluteTimeStamp, CNT, &TDC_data[0][0]);


		//manager->Pause();
		// Calculate the X, Y, Time of Flight, and Time_stamp

		u = (1 / 2) * ((TDC_data[0][0] * tdc_binsize) - (TDC_data[1][0] * tdc_binsize)) * fu;
		v = (1 / 2) * ((TDC_data[2][0] * tdc_binsize) - (TDC_data[3][0] * tdc_binsize)) * fv;
		w = (1 / 2) * (((TDC_data[4][0] * tdc_binsize) - (TDC_data[5][0] * tdc_binsize)) + w_offset) * fw;

		X = u;
		Y = (u - (2 * v)) / sqrt(3);
		TOF = abs((TDC_data[7][0] * tdc_binsize) - (TDC_data[6][0] * tdc_binsize));

		array_tem[0] = static_cast<double>(recorded_triggers);
		for (int i = 0; i < 12; ++i) {
			if (i < 8) {
				array_tem[(12 * (recorded_triggers - 1)) + i + 1] = static_cast<double>(TDC_data[i][0]);
			}
			else if (i == 8) {
				array_tem[(12 * (recorded_triggers - 1)) + i + 1] = X;
			}
			else if (i == 9) {
				array_tem[(12 * (recorded_triggers - 1)) + i + 1] = Y;
			}
			else if (i == 10) {
				array_tem[(12 * (recorded_triggers - 1)) + i + 1] = TOF;
			}
			else {
				array_tem[(12 * (recorded_triggers - 1)) + i + 1] = static_cast<double>(ui64_HPTDC_AbsoluteTimeStamp);
			}

		}

		if (recorded_triggers % buffer_size == 0) {
			break;
		}

		auto stop = high_resolution_clock::now();

		auto duration = duration_cast<microseconds>(stop - start);

		if (duration.count() == time_out_micro) {
			//cout << "Time taken by function: "
			//	<< duration.count() << " microseconds" << endl;
			break;
		}


	}
	return array_tem;
}


// Define C functions for the C++ class - as ctypes can only talk to C...
extern "C"
{
	__declspec(dllexport) Wrraper_tdc* Warraper_tdc_new(int buf_size, int time_out) { return new Wrraper_tdc(buf_size, time_out); }
	__declspec(dllexport) int init_tdc(Wrraper_tdc* Wrraper_tdc) { return Wrraper_tdc->init_tdc(); }
	__declspec(dllexport) int run_tdc(Wrraper_tdc* Wrraper_tdc) { return Wrraper_tdc->run_tdc(); }
	__declspec(dllexport) int stop_tdc(Wrraper_tdc* Wrraper_tdc) { return Wrraper_tdc->stop_tdc(); }
	__declspec(dllexport) double* get_data_tdc(Wrraper_tdc* Wrraper_tdc) { return Wrraper_tdc->get_data_tdc(); }
	__declspec(dllexport) double* get_data_tdc_buf(Wrraper_tdc* Wrraper_tdc) { return Wrraper_tdc->get_data_tdc_buf(); }
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


