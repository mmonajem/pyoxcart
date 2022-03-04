/********************************************************************\

  Name:         drs_ox.cpp
  Created by:   Mehrpad Monajem

  Contents:     A drs reader c++ file for creating dynamic library


\********************************************************************/

#include <math.h>

#include <windows.h>

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "strlcpy.h"
#include "DRS.h"
/*------------------------------------------------------------------*/

#include <iostream>
// A simple class with a constuctor and some methods...
class Drs_ox
{
    public:
       	Drs_ox(int, int, int, float);
        float* reader();
        void delete_drs_ox();
    private:
 	   DRS *drs;
 	   DRSBoard *b;
	   int i, j, nBoards;
		//   float wave_array[8][1024];
	   float array[8][1024];
	   float *array_tem = new float[1024*8];
};
Drs_ox::Drs_ox(int trigger, int test, int delay, float sample_frequency)
{
	   /* do initial scan */
	   drs = new DRS();

	   /* show any found board(s) */
	   b = drs->GetBoard(0);
	   printf("Found DRS4 evaluation board, serial #%d, firmware revision %d\n",
	         b->GetBoardSerialNumber(), b->GetFirmwareVersion());

	   /* exit if no board found */
	   nBoards = drs->GetNumberOfBoards();
	   if (nBoards == 0) {
	      printf("No DRS4 evaluation board found\n");
	   }

	   /* continue working with first board only */
	   b = drs->GetBoard(0);

	   /* initialize board */
	   b->Init();

	   /* set sampling frequency */
	   b->SetFrequency(sample_frequency, true);

	   /* enable transparent mode needed for analog trigger */
	   b->SetTranspMode(1);

	   /* set input range to -0.5V ... +0.5V */
	   b->SetInputRange(0);

	   /* use following line to set range to 0..1V */
	   //b->SetInputRange(0.5);

	   /* use following line to turn on the internal 100 MHz clock connected to all channels  */
	   if (test == 1) {
			  b->EnableTcal(1);
	   }
		  if (trigger == 0) {

		   }

	   /* use following lines to enable hardware trigger on CH1 at 50 mV positive edge */
	  if (trigger == 0) {
		   if (b->GetBoardType() >= 8) {        // Evaluaiton Board V4&5
				  b->EnableTrigger(1, 0);           // enable hardware trigger
				b->SetTriggerSource(1<<0);        // set CH1 as source
			  } else if (b->GetBoardType() == 7) { // Evaluation Board V3
				  b->EnableTrigger(0, 1);           // lemo off, analog trigger on
				 b->SetTriggerSource(0);           // use CH1 as source
			  }
	  }
	   b->SetTriggerLevel(0.05);            // 0.05 V
	   b->SetTriggerPolarity(false);        // positive edge

	   /* use following lines to set individual trigger elvels */
	   //b->SetIndividualTriggerLevel(1, 0.1);
	   //b->SetIndividualTriggerLevel(2, 0.2);
	   //b->SetIndividualTriggerLevel(3, 0.3);
	   //b->SetIndividualTriggerLevel(4, 0.4);
	   //b->SetTriggerSource(15);

	   b->SetTriggerDelayNs(delay);             // zero ns trigger delay

	   if (trigger == 1) {
		   /* use following lines to enable the external trigger */
		   if (b->GetBoardType() >= 8) {     // Evaluaiton Board V4
			   b->EnableTrigger(1, 0);           // enable hardware trigger
		     b->SetTriggerSource(1<<4);        // set external trigger as source
		   } else {                          // Evaluation Board V3
		      b->EnableTrigger(1, 0);           // lemo on, analog trigger off
		    }
	   }


}
float* Drs_ox::reader()
{
	  fflush(stdout);

      /* start board (activate domino wave) */
	  b->StartDomino();

	  /* wait for trigger */
//	  printf("Waiting for trigger...");

      fflush(stdout);
	  while (b->IsBusy());

	  /* read all waveforms */
	  b->TransferWaves(0, 8);

	  /* read time (X) array of first channel in ns */
	  b->GetTime(0, 0, b->GetTriggerCell(0), array[0]);

	  /* decode waveform (Y) array of first channel in mV */
	  b->GetWave(0, 0, array[1]);

	  /* read time (X) array of second channel in ns
	   Note: On the evaluation board input #1 is connected to channel 0 and 1 of
	   the DRS chip, input #2 is connected to channel 2 and 3 and so on. So to
	   get the input #2 we have to read DRS channel #2, not #1. */
	  b->GetTime(0, 2, b->GetTriggerCell(0), array[2]);

	  /* decode waveform (Y) array of second channel in mV */
	  b->GetWave(0, 2, array[3]);

	  /* channel 3*/
	  b->GetTime(0, 4, b->GetTriggerCell(0), array[4]);
	  b->GetWave(0, 4, array[5]);
	  /* channel 4*/
	  b->GetTime(0, 6, b->GetTriggerCell(0), array[6]);
	  b->GetWave(0, 6, array[7]);


	  /* print some progress indication */
//	  printf("\rEvent read successfully\n");


	   /* delete DRS object -> close USB connection */

//	   delete drs;
		for (i = 0; i < 8; ++i) {
			for (j = 0; j < 1024; ++j) {
				// mapping 1D array to 2D array
				array_tem[i * 1024 + j] = array[i][j];
			}
		}
	   return array_tem;
}

void Drs_ox::delete_drs_ox()
{
	/* delete DRS object -> close USB connection */
	delete drs;

}

// Define C functions for the C++ class - as ctypes can only talk to C...
extern "C"
{
    __declspec(dllexport) Drs_ox* Drs_new(int trigger, int test, int delay, float sample_frequency) {return new Drs_ox(trigger, test, delay, sample_frequency);}
    __declspec(dllexport) float* Drs_reader(Drs_ox* drs_ox) {return drs_ox->reader();}
    __declspec(dllexport) void Drs_delete_drs_ox(Drs_ox* drs_ox) {drs_ox->delete_drs_ox();}
}


