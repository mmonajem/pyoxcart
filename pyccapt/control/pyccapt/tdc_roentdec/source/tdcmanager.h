//
//TDC Manager header file for driver version 3.7.x (based on 3.5.x)
//

#ifdef HPTDC_DRIVER_EXPORTS
#define HPTDC_DRIVER_API __declspec(dllexport)
#else
#define HPTDC_DRIVER_API __declspec(dllimport)
#endif
#include <vector>
#include <string>

const int THROTTLE_ON_SIZE = 16384; 
const int THROTTLE_OFF_SIZE = 16384 + 16384;
#define THROTTLE 


#pragma warning(disable:4251)

using namespace std;
typedef unsigned short USHORT;
typedef unsigned long DWORD;
class TDC;
class Config;
typedef unsigned long HIT ;
class HPTDC_DRIVER_API  TDCConfigException {
public:
	const char * errorString;
	TDCConfigException(const char *error) {
		  errorString = error;
	}
};

	struct TDCHit {
	public:
		const static int RISING = 1;
		const static int FALLING = 0;
		const static int TDC_ERROR = 2;

		long long time;
		unsigned char channel;
		unsigned char type;
		unsigned short bin;
	};

/** This class contains the information about one TDC */
class TDCInfo {
public:
	int index;
	int channelStart;
	int channelCount;
	int highResChannelCount;
	int highResChannelStart;
	int lowResChannelCount;
	int lowResChannelStart;
	double resolution;
	DWORD serialNumber;
	
	int version;
	int fifoSize;
	int *INLCorrection;
	unsigned short *DNLData;
	bool flashValid;
	unsigned char boardConfiguration;
	unsigned short reserved2;
	int bufferSize;
};


const static int STATE_UNINITIALIZED = 0;
const static int STATE_NOT_CONFIGURED = 1;
const static int STATE_CONFIGURED = 2;
const static int STATE_RUNNING = 3;
const static int STATE_PAUSED = 4;
const static int STATE_SHUTDOWN = 5;


#include <iostream>
// This class manages multiple TDC, it can detect how many
// TDC are available and forwards the requests to the corresponding TDC
	class Frame;

class HPTDC_DRIVER_API TDCManager {
	TDC *tdcs[5];
	int tdcCount; 
    USHORT VendorID, DeviceID;
	volatile bool readThrottle;
	Config *config;
	bool groupingEnabled;
	bool externalClock;

	int state;
	bool configChanged;

	int tempIndex;
	int tempCount;
	struct TDCFrameState{
		Frame *frame;
		int position;
		int rollover;
		void clear() {
			rollover = 0;
			position = 1;
			frame = 0;
		}
	} ;

	TDCFrameState frameStates[5];


	int lastRolloverTime;
	int metaRolloverTime;
	// used for merging from multiple cards
	DWORD *mergeBuffers[5];
	int readCounts[5];
	// true if the data was read last time, and does not need to be restored
	bool mergeBufferCurrent[5];
	int TDCManager::ReadGroup(HIT *out, int size);

	bool tdcGreater(int i1, int i2);

	void tdcSwap(int i1, int i2);

	// init the default parameters
	static void TDCManager::initDefaultParameters(Config *config) ;

	void assertStopped();
	void assertState(int state, const char *text);
	void assertState(int state1, int state2, const char *text);
	void assertNotInState(int state, const char *text);

public:


	TDCManager(USHORT _VendorID = 0x1A13, USHORT _DeviceID = 0x0001);
	// Initializes the manager, by searching for PCI card and registering them
	// Reads the config and sets the registers
	void Init() ;	

	// Allows to initialize a subset of devices
	void Init(int startDevice, int deviceCount);	


	//the list of commands necessary for a readout
	void Start () ;

	// stops the readout
	void Stop () ;

	// suspends the readout temporarily
	void Pause () ;

	// return the driver version
	int getDriverVersion(); //DEPRECATED
	int GetDriverVersion() {
		return getDriverVersion();
	}
	// continues the readout
	void Continue () ;

	// Sets the registers in the HPTDC based on the config
	void Reconfigure();

	// sets a single parameter with key value
	bool SetParameter(const char * property, const char* value);

	// Sets a parameter like in the config file 
	bool SetParameter(const char * config);

	// reads config, returns false, if the file could not be found
	bool ReadConfigFile(const char * filename);

	// Reads the input of a string (may contain multiple parameters)
	bool ReadConfigString(const char *parameter);

	// The value of the parameter (result must not be freed)
	const char * GetParameter(const char *parameter);

	/** Returns all parameter names count contains the number of elements in array
	  the result must be freed with "delete[] params"*/
	const char ** GetParameterNames(int &count);

	//Stopps all processing and deallocate all resources
	void CleanUp () ;

	// reads data from the TDCs 
	int TDCManager::Read(HIT *out, int size);

	// Reads a hit as a struct (1ps resolution)
	int ReadTDCHit(TDCHit *buffer, int length);

	// Reads a hit as a struct (1ps resolution)
	int ReadTDCHitSince(TDCHit *buffer, int length, long long since);

		// reads data from the TDCs 
	int TDCManager::ReadNextFrame(HIT *out, int size);

	// converts a hit to text representation
	static string PrettyPrint(HIT hit);

	// prints into a buffer (no size check, min length > 200 bytes)
	static void PrettyPrint(HIT hit, char *buffer);
	
	// Returns information about the TDC
	TDCInfo getTDCInfo(int index);  //DEPRECATED
	TDCInfo GetTDCInfo(int index) {
		return getTDCInfo(index);
	}
	/** Clears all remaining data which is not yet read*/
	void ClearBuffer();

	/** Returns number of TDCs*/
	int getTDCCount() { //DEPRECATED
		assertNotInState(STATE_UNINITIALIZED, "Must call Init before requesting TDC count");
		return tdcCount;
	}
	int GetTDCCount() {
		assertNotInState(STATE_UNINITIALIZED, "Must call Init before requesting TDC count");
		return tdcCount;
	}
	// Get the state of the Manager see STATE_* constants
	int GetState() {
		return state; 
	}
	long long GetTDCStatusRegister(int index);  

	/***********************************************************
	* Internal methods 
	************************************************************/
	void TDCManager::EmergencyCleanUp();
	bool updateThrottle(bool value, int freeBuffer);
	void  PokeD(int index, int offset, DWORD value);
	DWORD PeekD(int index, int offset);
	// Internal Method write the flash 
	void WriteConfigFlash();
    
	// Internal Method, sets the serial number
	void SetTDCSerialNumber(int index, DWORD serialNumber);

	void SetMaxDevices(int deviceCount);
};
