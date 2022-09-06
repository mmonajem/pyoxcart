//----------------------------------------------------------------
//	© Thorlabs Limited.
//
//	FILE NAME       : APTAPI.h
//
//	AUTHOR          : Thorlabs Ltd, Ely, U.K.
//
//	CREATED         : 04-12-20
//
//	PLATFORM        : Win 32/64
//
//	MODULE FUNCTION:-
//
//	Defines WINAPI application programmers interface (exported by APT.DLL) for accessing
//	supported APT/Kinesis controllers/stages.
//
//	RELATED DOCUMENTATION:-
//
//	NOTES:-
//
//----------------------------------------------------------------
//	MODIFICATION HISTORY:-
//
//	DATE			VERSION
//
//	04-12-20		3.0.6
//
//	Significant extensions made to support additional motor controllers,
//	integrated stages, motorised flippers and inertial piezo controllers.
//	See lHWType definitons below for complete list of supported controllers/stages.
//	
//----------------------------------------------------------------

//#include <Windows.h>	// This may need uncommenting in some environments.

#ifdef __cplusplus
extern "C" {
#endif  /* __cplusplus */


// Define callback function type for a move complete.
typedef void(*pFnMoveCompleteCallback)(long, long);



// >>>>>>>>>>>>>>>>> MACRO DEFINITIONS <<<<<<<<<<<<<<<<<<

// lHWType definitions - used with GetNumHWUnitsEx & GetHWSerialNumEx.
//
// 'Prefix' refers to the hardware's serial number 2 digit prefix.

#define HWTYPE_BSC001		11		// Prefix 30 - Single channel benchtop stepper driver.
#define HWTYPE_BSC101		12		// Prefix 40 - Single channel benchtop stepper driver.
#define HWTYPE_BSC002		13		// Prefix 20 - Dual channel benchtop stepper driver.
#define HWTYPE_BDC101		14		// Prefix 43 - Single channel benchtop DC servo driver.
#define HWTYPE_SCC001		21		// Prefix 90 - Stepper driver channel (used within multi channel BSC benchtop units).
#define HWTYPE_DCC001		22		// Prefix 93 - DC servo driver channel (used within multi channel BDC benchtop units).
#define HWTYPE_ODC001		24		// Prefix 63 - Single channel DC servo driver cube.
#define HWTYPE_OST001		25		// Prefix 60 - Single channel stepper driver cube.
#define HWTYPE_MST601		26		// Prefix 50 - Dual channel stepper driver rack module.
#define HWTYPE_TST001		29		// Prefix 80 - Single channel stepper driver T-Cube.
#define HWTYPE_TDC001		31		// Prefix 83 - Single channel DC servo driver T-Cube.
#define HWTYPE_TSC001		33		// Prefix 85 - Single channel solenoid controller T-Cube.
#define HWTYPE_TIM001		40		// Prefix 65 - Single channel inertial driver T-Cube.
#define HWTYPE_LTSXXX		42		// Prefix 45 - LTS300/LTS150 long travel integrated driver/stages.
#define HWTYPE_L490MZ		43		// Prefix 46 - Integrated driver Labjack.
#define HWTYPE_BBD10X		44		// Prefix 94 - DC brushless servo driver channel (used in single and multi channel benchtop units)
#define HWTYPE_TBD001		45		// Prefix 67 - Single channel brushless servo driver T-Cube.
#define HWTYPE_FW105		46		// Prefix 47 - Integrated driver filter wheel.
#define HWTYPE_MLJ050		47		// Prefix 49 - Integrated driver Labjack.
#define HWTYPE_MFF10X		48		// Prefix 37 - Integrated driver filter flipper.
#define HWTYPE_K100CR1		50		// Prefix 55 - Integarted driver rotation stage.
#define HWTYPE_KST101		55		// Prefix 26 - Single channel stepper driver K-Cube.
#define HWTYPE_KSC101		57		// Prefix 68 - Single channel solenoid controller K-Cube.
#define HWTYPE_KIM101		60		// Prefix 97 - Quad channel inertial driver K-Cube.
#define HWTYPE_KIM001		61		// Prefix 74 - Single channel inertial driver K-Cube.
#define HWTYPE_KBD101		62		// Prefix 28 - Single channel brushless servo driver K-Cube.
#define HWTYPE_KDC101		63		// Prefix 27 - Single channel DC servo driver K-Cube.


// >>>> Constant definitions for MOT_ prefixed exported functions <<<<

// Channel idents - used with MOT_SetChannel.
#define CHAN1_INDEX			0		// 04-12-20 - Deprecated >> Channel 1.
#define CHAN2_INDEX			1		// 04-12-20 - Deprecated >> Channel 2.
#define MOT_CHAN1_INDEX		0		// Channel 1.
#define MOT_CHAN2_INDEX		1		// Channel 2.

// Home direction (lDirection) - used with MOT_Set(Get)HomeParams.
#define HOME_FWD			1		// 04-12-20 - Deprecated >> Home in the forward direction.
#define HOME_REV			2		// 04-12-20 - Deprecated >> Home in the reverse direction.
#define MOT_HOME_FWD		1		// Home in the forward direction.
#define MOT_HOME_REV		2		// Home in the reverse direction.

// Home limit switch (lLimSwitch) - used with MOT_Set(Get)HomeParams.
#define HOMELIMSW_FWD			4		// 04-12-20 - Deprecated >> Use forward limit switch for home datum.
#define HOMELIMSW_REV			1		// 04-12-20 - Deprecated >> Use reverse limit switch for home datum.
#define MOT_HOMELIMSW_FWD		4		// Use forward limit switch for home datum.
#define MOT_HOMELIMSW_REV		1		// Use reverse limit switch for home datum.

// Jogging mode (lMode) - used with MOT_Set(Get)JogParams.
#define MOT_JOG_CONTINUOUS		1	// Move continuously when jog commanded.
#define MOT_JOG_SINGLESTEP		2	// Move one jog step (fStepSize) when jog commanded.

// Jog stop mode (lStopMode) - used with MOT_Set(Get)JogParams.
#define MOT_JOGSTOP_IMMEDIATE	1	// Stops the move immediately.
#define MOT_JOGSTOP_PROFILED	2	// Stops the move in a controlled deceleration.

// Stage units (lUnits) - used with MOT_Set(Get)StageAxisInfo.
#define STAGE_UNITS_MM		1		// 04-12-20 - Deprecated >> Stage units are in mm.
#define STAGE_UNITS_DEG		2		// 04-12-20 - Deprecated >> Stage units are in degrees.
#define MOT_STAGE_UNITS_MM		1	// Stage units are in mm.
#define MOT_STAGE_UNITS_DEG		2	// Stage units are in degrees.

// Hardware limit switch settings (lRevLimSwitch, lFwdLimSwitch) - used with MOT_Set(Get)HWLimSwitches
#define HWLIMSWITCH_IGNORE					1		// 04-12-20 - Deprecated >> Ignore limit switch (e.g. for stages with only one or no limit switches).
#define HWLIMSWITCH_MAKES					2		// 04-12-20 - Deprecated >> Limit switch is activated when electrical continuity is detected.
#define HWLIMSWITCH_BREAKS					3		// 04-12-20 - Deprecated >> Limit switch is activated when electrical continuity is broken.
#define HWLIMSWITCH_MAKES_HOMEONLY			4		// 04-12-20 - Deprecated >> As per HWLIMSWITCH_MAKES except switch is ignored other than when homing (e.g. to support rotation stages).
#define HWLIMSWITCH_BREAKS_HOMEONLY			5		// 04-12-20 - Deprecated >> As per HWLIMSWITCH_BREAKS except switch is ignored other than when homing (e.g. to support rotation stages).
#define MOT_HWLIMSWITCH_IGNORE				1		// Ignore limit switch (e.g. for stages with only one or no limit switches).
#define MOT_HWLIMSWITCH_MAKES				2		// Limit switch is activated when electrical continuity is detected.
#define MOT_HWLIMSWITCH_BREAKS				3		// Limit switch is activated when electrical continuity is broken.
#define MOT_HWLIMSWITCH_MAKES_HOMEONLY		4		// As per HWLIMSWITCH_MAKES except switch is ignored other than when homing (e.g. to support rotation stages).
#define MOT_HWLIMSWITCH_BREAKS_HOMEONLY		5		// As per HWLIMSWITCH_BREAKS except switch is ignored other than when homing (e.g. to support rotation stages).

// Move direction (lDirection) - used with MOT_MoveVelocity.
#define MOVE_FWD			1		// 04-12-20 - Deprecated >> Move forward.
#define MOVE_REV			2		// 04-12-20 - Deprecated >> Move reverse.
#define MOT_MOVEVEL_FWD		1		// Move at velocity forward.
#define MOT_MOVEVEL_REV		2		// Move at velocity reverse.

// Jog direction (lJogDir) - used with MOT_MoveJog.
#define MOT_JOGFWD			1		// Jog forward.
#define MOT_JOGREV			2		// Jog reverse.

// Rotation move mode (lMoveMode) - used with MOT_MoveAbsoluteRot.
#define MOT_ROTMOVE_POS			1		// Always move in the clockwise direction.
#define MOT_ROTMOVE_NEG			2		// Always move in the anti-clockwise direction.
#define MOT_ROTMOVE_SHORT		3		// Always do the shortest move.

// DC motor profile mode (lProfMode) - used with MOT_Set(Get)DCProfileModeParams.
#define DC_PROFILEMODE_TRAPEZOIDAL			0		// 04-12-20 - Deprecated >> Trapezoidal move trajectory.
#define DC_PROFILEMODE_SCURVE				2		// 04-12-20 - Deprecated >> S Curve move trajectory.
#define MOT_DC_PROFILEMODE_TRAPEZOIDAL		0		// Trapezoidal move trajectory.
#define MOT_DC_PROFILEMODE_SCURVE			2		// S Curve move trajectory.

// DC motor joystick direction sense settings (lDirSense) - used with MOT_Set(Get)DCJoystickParams.
#define DC_JS_DIRSENSE_POS				1		// 04-12-20 - Deprecated >> Positive direction sense.
#define DC_JS_DIRSENSE_NEG				2		// 04-12-20 - Deprecated >> Negative direction sense.
#define MOT_DC_JS_DIRSENSE_POS			1		// Positive direction sense.
#define MOT_DC_JS_DIRSENSE_NEG			2		// Negative direction sense.

// DC motor triggering parameters (lTrigInMode, lTrigOutMode) - used with MOT_Set(Get)DCTriggerParams
#define MOT_DC_TRIGIN_DISABLED				1		// Input trigger desabled.
#define MOT_DC_TRIGINHIGH_RELMOVE			2		// Trigger a relative move on rising edge.
#define MOT_DC_TRIGINLOW_RELMOVE			3		// Trigger a relative move on falling edge.
#define MOT_DC_TRIGINHIGH_ABSMOVE			4		// Trigger an absolute move on rising edge.
#define MOT_DC_TRIGINLOW_ABSMOVE			5		// Trigger an absolute move on falling edge.
#define MOT_DC_TRIGINHIGH_HOMEMOVE			6		// Trigger a homing move on rising edge.
#define MOT_DC_TRIGINLOW_HOMEMOVE			7		// Trigger a homing move on falling edge.

#define MOT_DC_TRIGOUT_DISABLED				1		// Output trigger disabled.
#define MOT_DC_TRIGOUTHIGH_INMOTION			2		// Outout trigger set to logic HIGH when system in motion.
#define MOT_DC_TRIGOUTLOW_INMOTION			3		// Output trigger set to logic LOW when system in motion.
#define MOT_DC_TRIGOUTHIGH_MOTIONCOMPLETE	4		// Outout trigger set to logic HIGH when motion stopped.
#define MOT_DC_TRIGOUTLOW_MOTIONCOMPLETE	5		// Outout trigger set to logic LOW when motion stopped.
#define MOT_DC_TRIGOUTHIGH_MAXVELOCITY		6		// Outout trigger set to logic HIGH when system at maximum velocity.
#define MOT_DC_TRIGOUTLOW_MAXVELOCITY		7		// Outout trigger set to logic LOW when system in motion.

// K-Cube top panel wheel mode (lWheelMode) - used with MOT_Set(Get)KCubePanelParams.
#define KMOT_WHL_VELOCITY				1		// Wheel (pot) used in velocity control mode.
#define KMOT_WHL_JOG					2		// Wheel (pot) used for jogging.
#define KMOT_WHL_GOTOPOSITION			3		// Wheel (pot) used to move to either preset position (fPresentPos1, fPresetPos2).

// K-Cube top panel wheel direction sense (lWheelDirSense) - used with MOT_Set(Get)KCubePanelParams.
#define KMOT_WHL_DIRSENSE_DISABLED		0		// Disables the wheel.
#define KMOT_WHL_DIRSENSE_POS			1		// Upwards rotation of wheel results in positive motion (increasing position count).
#define KMOT_WHL_DIRSENSE_NEG			2		// Upwards rotation of wheel results in negative motion (decreasing position count).

// K-Cube triggering mode (lTrig1Mode, lTrig2Mode) - used with MOT_Set(Get)KCubeTriggerParams.
#define KMOT_TRIG_ISDISABLED			0		// Trigger port disabled.

#define KMOT_TRIGIN_GPI					1		// General purpose logic input (read through status bits by calling MOT_GetStatusBits).
#define KMOT_TRIGIN_RELMOVE				2		// Input trigger to make relative move.
#define KMOT_TRIGIN_ABSMOVE				3		// Input trigger to make absolute move.
#define KMOT_TRIGIN_HOME				4		// Input trigger to make home move.

#define KMOT_TRIGOUT_GPO				10		// General purpose logic output (set by calling MOT_LLSetGetDigOPs).
#define KMOT_TRIGOUT_INMOTION			11		// Output active (level) when motor 'in motion'.
#define KMOT_TRIGOUT_MAXVELOCITY		12		// Output active (level) when motor at 'maximum velocity'.
// Only one trigger port can be set to any of the 6 following modes.
#define KMOT_TRIGOUT_POSSTEPS_FWD		13		// Output active (pulsed) at pre-defined positions moving forward (specified using MOT_SetKCubePosTriggerParams).
#define KMOT_TRIGOUT_POSSTEPS_REV		14		// Output active (pulsed) at pre-defined positions moving backwards (specified using MOT_SetKCubePosTriggerParams).
#define KMOT_TRIGOUT_POSSTEPS_BOTH		15		// Output active (pulsed) at pre-defined positions moving forwards and backwards (specified using MOT_SetKCubePosTriggerParams).
#define KMOT_TRIGOUT_FWDLIMIT			16		// Output active (level) when forward limit switch is activated. 
#define KMOT_TRIGOUT_REVLIMIT			17		// Output active (level) when reverse limit switch is activated.
#define KMOT_TRIGOUT_EITHERLIMIT		18		// Output active (level) when either the forward or the reverse limit switch is activated.

// K-Cube trigger port polarity (lTrig1Polarity, lTrig2Polarity) - used with MOT_Set(Get)KCubeTriggerParams.
#define KMOT_TRIG_POLHIGH				1		// The 'active' state of the trigger port is logic HIGH (i.e. trigger input and output on a rising edge).
#define KMOT_TRIG_POLLOW				2		// The 'active' state of the trigger port is logic LOW (i.e. trigger input and output on a falling edge).

// KST101 loop mode (lLoopMode) - used with MOT_Set(Get)KCubeKSTLoopParams.
#define KMOT_KST_OPENLOOP				1		// Sets open loop positioning.
#define KMOT_KST_CLOSEDLOOP				2		// Sets closed loop positioning.


// >>>> Constant definitions for MFF_ prefixed exported functions <<<<

// Jog direction (lJogDir) - used with MFF_MoveJog.
#define MFF_JOGFWD			1		// Jog forward (goto flipper position 1).
#define MFF_JOGREV			2		// Jog reverse (goto flipper position 2).

// Digital I/O connector operating mode (lDigIO1OperMode, lDigIO2OperMode) - used with MFF_Set(Get)MFFOperParams.
#define MFF_OPMODE_IP_TOGGLEPOS			1		// Sets IO connector to input and 'toggle position' mode (input signal causes flipper to move to other position).
#define MFF_OPMODE_IP_GOTOPOS			2		// Sets IO connector to input and 'goto position' mode (input signal dictates flipper position, position 1 or 2).
#define MFF_OPMODE_OP_ATPOS				3		// Sets IO connector to output where signal indicates flipper at position.
#define MFF_OPMODE_OP_MOVING			4		// Sets IO connector to output where signal indicates flipper is in motion (between positions).

// Digital I/O connector signal mode (lDigIO1SigMode, lDigIO2SigMode) - used with MFF_Set(Get)MFFOperParams.
#define MFF_SIGNALMODE_IP_BUTTON		1		// Connector can be short circuited (e.g. with button) to provide signal.
#define MFF_SIGNALMODE_IP_LOGIC			2		// Connector is set to logic input where a logic transition (edge) dictates flipper operation. 
#define MFF_SIGNALMODE_IP_SWAP			4		// Bitwise OR with any of the IP SIGMODEs above to swap flipper position 1 2 (i.e. reverse operation).
#define MFF_SIGNALMODE_OP_LEVEL			16		// Connector is set to a logic output where the logic transition (edge) indicates flipper state.
#define MFF_SIGNALMODE_OP_PULSE			32		// Connector is set to a logic output where a logic pulse (width specified by lDigIO1PulseWidth and lDigIO2PulseWidth) indicates flipper state.
#define MFF_SIGNALMODE_OP_INVERT		64		// Bitwise OR with any of the OP SIGMODEs above to invert the logic levels for the operations described.


// >>>> Constant definitions for SC_ prefixed exported functions <<<<

// Solenoid operating mode (lMode) - used with SC_Set(Get)OperatingMode.
#define SC_MANUAL		1		// Toggle solenoid on/off state using enable button/command.
#define SC_SINGLE		2		// Initiate solenoid on/off cycle using enable button/command.
#define SC_AUTO			3		// Initiate repeated solenoid on/off cycles using enable button/command.
#define SC_TRIGGER		4		// Enable input hardware triggering (output trigger mirrored).


// >>>> Constant definitions for PZMOT_ prefixed exported functions <<<<

// Jog operating mode (lMode) - used with PZMOT_Set(Get)JogMode.
#define PZMOT_JOG_CONTINUOUS			1		// Move continuously while jog signal present.
#define PZMOT_JOG_SINGLESTEP			2		// Move one jog step (set using PZMOT_SetJogStepSize) when jog signal detected.  

// TIM001 button operating mode (lMode) - used with PZMOT_Set(Get)ButtonParams.
#define PZMOT_BUTTON_JOG				1		// Buttons used for jogging.
#define PZMOT_BUTTON_POSITION			2		// Buttons used for going to preset positions.

// K-Cube top panel joystick (wheel on KIM001) mode (lJSMode) - PZMOT_Set(Get)KCubePanelParamss.
#define KPZMOT_JOY_VELOCITY				1		// Joystick used in velocity control mode.
#define KPZMOT_JOY_JOG					2		// Joystick used for jogging.
#define KPZMOT_JOY_GOTOPOSITION			3		// Joystick used to move to either preset position (lPresentPos1, lPresetPos2).

// K-Cube top panel joystick (wheel on KIM001) direction sense (lJSDirSense) - used with PZMOT_Set(Get)KCubePanelParamss.
#define KPZMOT_JOY_DIRSENSE_DISABLED	0		// Disables the joystick.
#define KPZMOT_JOY_DIRSENSE_POS			1		// Up/right deflection of joystick results in positive motion (i.e. increasing position count).
#define KPZMOT_JOY_DIRSENSE_NEG			2		// Up/right deflection of joystick results in negative motion (i.e. decreasing position count).

// K-Cube trigger channels (lTrigChan1, lTrig2Chan1) - used with PZMOT_Set(Get)KCubeTriggerParams.
#define KPZMOT_CHAN1			1	// Specificed trigger connector (I/O 1 or I/O 2) associated with drive channel 1.
#define KPZMOT_CHAN2			2	// Specificed trigger connector (I/O 1 or I/O 2) associated with drive channel 2.
#define KPZMOT_CHAN3			4	// Specificed trigger connector (I/O 1 or I/O 2) associated with drive channel 3.
#define KPZMOT_CHAN4			8	// Specificed trigger connector (I/O 1 or I/O 2) associated with drive channel 4.

// K-Cube triggering mode (lTrig1Mode, lTrig2Mode) - used with PZMOT_Set(Get)KCubeTriggerParams.
#define KPZMOT_TRIG_ISDISABLED				0		// Trigger (I/O) port disabled.

#define KPZMOT_TRIG_IN_GPI					1		// General puporse logic input (read through status bits by calling MOT_GetStatusBits).
#define KPZMOT_TRIG_IN_RELMOVE				2		// Input trigger to make relative move.
#define KPZMOT_TRIG_IN_ABSMOVE				3		// Input trigger to make absolute move.
#define KPZMOT_TRIG_IN_RESETCOUNT			4		// Input trigger to reset position counter to zero (e.g. at home position).

#define KPZMOT_TRIG_OUT_GPO					10		// General purpose logic output (set by calling PZMOT_LLSetGetDigOPs).
#define KPZMOT_TRIG_OUT_INMOTION			11		// Output active (level) when motor 'in motion'.
#define KPZMOT_TRIG_OUT_MAXVELOCITY			12		// Output active (level) when motor at 'max velocity'.

// Only one trigger port can be set to any of the 6 following modes.
#define KPZMOT_TRIG_OUT_POSSTEPS_FWD		13		// Output active (pulsed) at pre-defined positions moving forward (specified using PZMOT_SetKCubePosTriggerParams).
#define KPZMOT_TRIG_OUT_POSSTEPS_REV		14		// Output active (pulsed) at pre-defined positions moving backwards (specified using PZMOT_SetKCubePosTriggerParams).
#define KPZMOT_TRIG_OUT_POSSTEPS_BOTH		15		// Output active (pulsed) at pre-defined positions moving forwards and backwards (specified using PZMOT_SetKCubePosTriggerParams).
#define KPZMOT_TRIG_OUT_FWDLIMIT			16		// Output active (level) when forward limit switch is activated. 
#define KPZMOT_TRIG_OUT_REVLIMIT			17		// Output active (level) when reverse limit switch is activated.
#define KPZMOT_TRIG_OUT_EITHERLIMIT			18		// Output active (level) when either the forward or the reverse limit switch is activated.

// K-Cube trigger port polarity (lTrig1Polarity, lTrig2Polarity) - used with PZMOT_Set(Get)KCubeTriggerParams.
#define KPZMOT_TRIG_POLHIGH			1		// The 'active' state of the trigger port is logic HIGH (i.e. trigger input and output on a rising edge).
#define KPZMOT_TRIG_POLLOW			2		// The 'active' state of the trigger port is logic LOW (i.e. trigger input and output on a falling edge).

// K-Cube channel enable mode (lMode) - used with PZMOT_Set(Get)KCubeChanEnableMode.
#define PZMOT_ENABLE_NONE			0		// Disable output channels.
#define PZMOT_ENABLE_SINGLE1		1		// Enable output channel 1.
#define PZMOT_ENABLE_SINGLE2		2		// Enable output channel 2.
#define PZMOT_ENABLE_SINGLE3		3		// Enable output channel 3.
#define PZMOT_ENABLE_SINGLE4		4		// Enable output channel 4.
#define PZMOT_ENABLE_PAIR_12		5		// Enable output channels 1 and 2 as a connected pair (e.g. when using the joystick).
#define PZMOT_ENABLE_PAIR_34		6		// Enable output channels 3 and 4 as a connected pair (e.g. when using the koystick).

// K-Cube jogging mode (lJogMode) - used with PZMOT_Set(Get)KCubeJogParams.
#define PZMOT_JOG_CONTINUOUS		1		// Move continuously while jog signal present.
#define PZMOT_JOG_SINGLESTEP		2		// Move one jog step (set using PZMOT_SetJogStepSize) when jog signal detected.  

// K-Cube feedback signal mode (lFBMode) - used with PZMOT_Set(Get)KCubeFeedbackSig.
#define PZMOT_KIMFB_NOINPUT			0		// No feedback
#define PZMOT_KIMFB_LIMSSWITCH		1		// Feedback input connected to limit switch.
#define PZMOT_KIMFB_ENCODER			2		// Feedback input connected to encoder.

// Move at velocity direction (lDirection) - used with PZMOT_MoveVelocity.
#define PZMOT_MOVEVEL_FWD		1		// Move at velocity forward.
#define PZMOT_MOVEVEL_REV		2		// Move at velocity reverse.

// Jog direction (lJogDir) - used with PZMOT_MoveJog.
#define PZMOT_JOGFWD			1		// Jog forward.
#define PZMOT_JOGREV			2		// Jog reverse.


// >>>>>>>>>>>>>>>>> EXPORTED FUNCTIONS <<<<<<<<<<<<<<<<<<

// >>>>>>>> System level exports <<<<<<<<<

long WINAPI APTInit(void);
long WINAPI APTCleanUp(void);
long WINAPI GetNumHWUnitsEx(long lHWType, long *plNumUnits);
long WINAPI GetHWSerialNumEx(long lHWType, long lIndex, long *plSerialNum);
long WINAPI GetHWInfo(long lSerialNum, TCHAR *szModel, long lModelLen, TCHAR *szSWVer, long lSWVerLen, TCHAR *szHWNotes, long lHWNotesLen);
long WINAPI InitHWDevice(long lSerialNum);
long WINAPI EnableEventDlg(BOOL bEnable);
long WINAPI DoEvents(void);


// >>>>>>>>>> Motor Controller Related Exports <<<<<<<<<<<

long WINAPI MOT_ConnectHomeCompleteCallback(long lSerialNum, pFnMoveCompleteCallback pFnHomeCallback);
long WINAPI MOT_DisconnectHomeCompleteCallback(long lSerialNum, pFnMoveCompleteCallback pFnHomeCallback);
long WINAPI MOT_ConnectMoveCompleteCallback(long lSerialNum, pFnMoveCompleteCallback pFnMoveCallback);
long WINAPI MOT_DisconnectMoveCompleteCallback(long lSerialNum, pFnMoveCompleteCallback pFnMoveCallback);

long WINAPI MOT_LLSetEncoderCount(long lSerialNum, long lEncCount);
long WINAPI MOT_LLGetEncoderCount(long lSerialNum, long *plEncCount);
long WINAPI MOT_LLSetGetDigOPs(long lSerialNum, BOOL bSet, long *plBits);
long WINAPI MOT_LLGetADCInputs(long lSerialNum, long *plADCVal1, long *plADCVal2);

long WINAPI MOT_SetChannel(long lSerialNum, long lChanID);
long WINAPI MOT_Identify(long lSerialNum);
long WINAPI MOT_EnableHWChannel(long lSerialNum);
long WINAPI MOT_DisableHWChannel(long lSerialNum);
long WINAPI MOT_SetVelParams(long lSerialNum, float fMinVel, float fAccn, float fMaxVel);
long WINAPI MOT_GetVelParams(long lSerialNum, float *pfMinVel, float *pfAccn, float *pfMaxVel);
long WINAPI MOT_GetVelParamLimits(long lSerialNum, float *pfMaxAccn, float *pfMaxVel);
long WINAPI MOT_SetHomeParams(long lSerialNum, long lDirection, long lLimSwitch, float fHomeVel, float fZeroOffset);
long WINAPI MOT_GetHomeParams(long lSerialNum, long *plDirection, long *plLimSwitch, float *pfHomeVel, float *pfZeroOffset);
long WINAPI MOT_SetJogParams(long lSerialNum, long lMode, long lStopMode, float fStepSize, float fMinVel, float fAccn, float fMaxVel);
long WINAPI MOT_GetJogParams(long lSerialNum, long *plMode, long *plStopMode, float *pfStepSize, float *pfMinVel, float *pfAccn, float *pfMaxVel);
long WINAPI MOT_GetStatusBits(long lSerialNum, long *plStatusBits);
long WINAPI MOT_SetBLashDist(long lSerialNum, float fBLashDist);
long WINAPI MOT_GetBLashDist(long lSerialNum, float *pfBLashDist);
long WINAPI MOT_SetMotorParams(long lSerialNum, long lStepsPerRev, long lGearBoxRatio);
long WINAPI MOT_GetMotorParams(long lSerialNum, long *plStepsPerRev, long *plGearBoxRatio);
long WINAPI MOT_SetStageAxisInfo(long lSerialNum, float fMinPos, float fMaxPos, long lUnits, float fPitch);
long WINAPI MOT_GetStageAxisInfo(long lSerialNum, float *pfMinPos, float *pfMaxPos, long *plUnits, float *pfPitch);
long WINAPI MOT_SetHWLimSwitches(long lSerialNum, long lRevLimSwitch, long lFwdLimSwitch);
long WINAPI MOT_GetHWLimSwitches(long lSerialNum, long *plRevLimSwitch, long *plFwdLimSwitch);
long WINAPI MOT_SetPIDParams(long lSerialNum, long lProp, long lInt, long lDeriv, long lIntLimit);
long WINAPI MOT_GetPIDParams(long lSerialNum, long *plProp, long *plInt, long *plDeriv, long *plIntLimit);
long WINAPI MOT_SetPhaseCurrents(long lSerialNum, long lRestVal, long lMoveVal);
long WINAPI MOT_GetPhaseCurrents(long lSerialNum, long *plRestVal, long *plMoveVal);
long WINAPI MOT_GetPosition(long lSerialNum, float *pfPosition);
long WINAPI MOT_GetPositionEx(long lSerialNum, float *pfCalibPosition, float *pfUncalibPosition);
long WINAPI MOT_MoveHome(long lSerialNum, BOOL bWait);
long WINAPI MOT_MoveRelativeEx(long lSerialNum, float fRelDist, BOOL bWait);
long WINAPI MOT_MoveAbsoluteEx(long lSerialNum, float fAbsPos, BOOL bWait);
long WINAPI MOT_MoveVelocity(long lSerialNum, long lDirection);
long WINAPI MOT_MoveJog(long lSerialNum, long lJogDir);
long WINAPI MOT_MoveAbsoluteRot(long lSerialNum, float fAnglePos, long lMoveMode, BOOL bWait);
long WINAPI MOT_StopProfiled(long lSerialNum);
long WINAPI MOT_SetDCCurrentLoopParams(long lSerialNum, long lProp, long lInt, long lIntLim, long lIntDeadBand, long lFFwd);
long WINAPI MOT_GetDCCurrentLoopParams(long lSerialNum, long *plProp, long *plInt, long *plIntLim, long *plIntDeadBand, long *plFFwd);
long WINAPI MOT_SetDCPositionLoopParams(long lSerialNum, long lProp, long lInt, long lIntLim, long lDeriv, long lDerivTime, long lLoopGain, long lVelFFwd, long lAccFFwd, long lPosErrLim);
long WINAPI MOT_GetDCPositionLoopParams(long lSerialNum, long *plProp, long *plInt, long *plIntLim, long *plDeriv, long *plDerivTime, long *plLoopGain, long *plVelFFwd, long *plAccFFwd, long *plPosErrLim);
long WINAPI MOT_SetDCMotorOutputParams(long lSerialNum, float fContCurrLim, float fEnergyLim, float fMotorLim, float fMotorBias);
long WINAPI MOT_GetDCMotorOutputParams(long lSerialNum, float *pfContCurrLim, float *pfEnergyLim, float *pfMotorLim, float *pfMotorBias);
long WINAPI MOT_SetDCTrackSettleParams(long lSerialNum, long lSettleTime, long lSettleWnd, long lTrackWnd);
long WINAPI MOT_GetDCTrackSettleParams(long lSerialNum, long *plSettleTime, long *plSettleWnd, long *plTrackWnd);
long WINAPI MOT_SetDCProfileModeParams(long lSerialNum, long lProfMode, float fJerk);
long WINAPI MOT_GetDCProfileModeParams(long lSerialNum, long *plProfMode, float *pfJerk);
long WINAPI MOT_SetDCJoystickParams(long lSerialNum, float fMaxVelLO, float fMaxVelHI, float fAccnLO, float fAccnHI, long lDirSense);
long WINAPI MOT_GetDCJoystickParams(long lSerialNum, float *pfMaxVelLO, float *pfMaxVelHI, float *pfAccnLO, float *pfAccnHI, long *plDirSense);
long WINAPI MOT_SetDCSettledCurrentLoopParams(long lSerialNum, long lSettledProp, long lSettledInt, long lSettledIntLim, long lSettledIntDeadBand, long lSettledFFwd);
long WINAPI MOT_GetDCSettledCurrentLoopParams(long lSerialNum, long *plSettledProp, long *plSettledInt, long *plSettledIntLim, long *plSettledIntDeadBand, long *plSettledFFwd);
long WINAPI MOT_SetBowIndex(long lSerialNum, long lBowIndex);
long WINAPI MOT_GetBowIndex(long lSerialNum, long *plBowIndex);
long WINAPI MOT_SetDCTriggerParams(long lSerialNum, long lTrigInMode, long lTrigOutMode);
long WINAPI MOT_GetDCTriggerParams(long lSerialNum, long *plTrigInMode, long *plTrigOutMode);
long WINAPI MOT_SetKCubePanelParams(long lSerialNum, long lWheelMode, float fWheelVel, float fWheelAccn, long lWheelDirSense, float fPresetPos1, float fPresetPos2, long lDispBrightness);
long WINAPI MOT_GetKCubePanelParams(long lSerialNum, long *plWheelMode, float *pfWheelVel, float *pfWheelAccn, long *plWheelDirSense, float *pfPresetPos1, float *pfPresetPos2, long *plDispBrightness);
long WINAPI MOT_SetKCubeTriggerParams(long lSerialNum, long lTrig1Mode, long lTrig1Polarity, long lTrig2Mode, long lTrig2Polarity);
long WINAPI MOT_GetKCubeTriggerParams(long lSerialNum, long *plTrig1Mode, long *plTrig1Polarity, long *plTrig2Mode, long *plTrig2Polarity);
long WINAPI MOT_SetKCubePosTriggerParams(long lSerialNum, float fStartPosFwd, float fPosIntervalFwd, long lNumPulsesFwd, float fStartPosRev, float fPosIntervalRev, long lNumPulsesRev, float fPulseWidth, long lNumCycles);
long WINAPI MOT_GetKCubePosTriggerParams(long lSerialNum, float *pfStartPosFwd, float *pfPosIntervalFwd, long *plNumPulsesFwd, float *pfStartPosRev, float *pfPosIntervalRev, long *plNumPulsesRev, float *pfPulseWidth, long *plNumCycles);
long WINAPI MOT_SetKCubeKSTLoopParams(long lSerialNum, long lLoopMode, long lProp, long lInt, long lDiff, long lPIDClip, long lPIDTol, long lEncConst);
long WINAPI MOT_GetKCubeKSTLoopParams(long lSerialNum, long *plLoopMode, long *plProp, long *plInt, long *plDiff, long *plPIDClip, long *lPIDTol, long *plEncConst);
long WINAPI MOT_GetInMotion(long lSerialNum, BOOL *pbInMotionFlag);


// >>>>>>>>>>>> Motorised Flipper Related Exports <<<<<<<<<<<<<

long WINAPI MFF_Identify(long lSerialNum);
long WINAPI MFF_EnableHWChannel(long lSerialNum);
long WINAPI MFF_DisableHWChannel(long lSerialNum);
long WINAPI MFF_MoveJog(long lSerialNum, long lJogDir);
long WINAPI MFF_SetMFFOperParams(long lSerialNum, long lTransitTime, long lDigIO1OperMode, long lDigIO1SigMode, long lDigIO1PulseWidth, long lDigIO2OperMode, long lDigIO2SigMode, long lDigIO2PulseWidth);
long WINAPI MFF_GetMFFOperParams(long lSerialNum, long *plTransitTime, long *plDigIO1OperMode, long *plDigIO1SigMode, long *plDigIO1PulseWidth, long *plDigIO2OperMode, long *plDigIO2SigMode, long *plDigIO2PulseWidth);
long WINAPI MFF_GetStatusBits(long lSerialNum, long *plStatusBits);


// >>>>>>>>>>>> Solenoid Controler Related Exports <<<<<<<<<<<<<

long WINAPI SC_Identify(long lSerialNum);
long WINAPI SC_SetOperatingMode(long lSerialNum, long lMode);
long WINAPI SC_GetOperatingMode(long lSerialNum, long *plMode);
long WINAPI SC_SetCycleParams(long lSerialNum, float fOnTime, float fOffTime, long lNumCycles);
long WINAPI SC_GetCycleParams(long lSerialNum, float *pfOnTime, float *pfOffTime, long *plNumCycles);
long WINAPI SC_Enable(long lSerialNum);
long WINAPI SC_Disable(long lSerialNum);
long WINAPI SC_GetOPState(long lSerialNum, long *plState);
long WINAPI SC_GetStatusBits(long lSerialNum, long *plStatusBits);


// >>>>>>>>>>>> Piezo Motor Related Exports <<<<<<<<<<<<<

long WINAPI PZMOT_ConnectMoveCompleteCallback(long lSerialNum, pFnMoveCompleteCallback pFnMoveCallback);
long WINAPI PZMOT_DisconnectMoveCompleteCallback(long lSerialNum, pFnMoveCompleteCallback pFnMoveCallback);

long WINAPI PZMOT_LLSetGetDigOPs(long lSerialNum, BOOL bSet, long *plBits);

long WINAPI PZMOT_SetChannel(long lSerialNum, long lChanID);
long WINAPI PZMOT_Identify(long lSerialNum);
long WINAPI PZMOT_EnableHWChannel(long lSerialNum);
long WINAPI PZMOT_SetDriveOPParams(long lSerialNum, long lVoltage, long lStepRate, long lStepAccn);
long WINAPI PZMOT_GetDriveOPParams(long lSerialNum, long *plVoltage, long *plStepRate, long *plStepAccn);
long WINAPI PZMOT_SetJogMode(long lSerialNum, long lMode);
long WINAPI PZMOT_GetJogMode(long lSerialNum, long *plMode);
long WINAPI PZMOT_SetJogStepSize(long lSerialNum, long lJogSteps);
long WINAPI PZMOT_GetJogStepSize(long lSerialNum, long *plJogSteps);
long WINAPI PZMOT_SetJogOPParams(long lSerialNum, long lStepRate, long lStepAccn);
long WINAPI PZMOT_GetJogOPParams(long lSerialNum, long *plStepRate, long *plStepAccn);
long WINAPI PZMOT_SetPositionSteps(long lSerialNum, long lPosSteps);
long WINAPI PZMOT_GetPositionSteps(long lSerialNum, long *plPosSteps);
long WINAPI PZMOT_SetButtonParams(long lSerialNum, long lButMode, long lButPos1, long lButPos2);
long WINAPI PZMOT_GetButtonParams(long lSerialNum, long *plButMode, long *plButPos1, long *plButPos2);
long WINAPI PZMOT_SetPotParams(long lSerialNum, long lMaxStepRate);
long WINAPI PZMOT_GetPotParams(long lSerialNum, long *plMaxStepRate);
long WINAPI PZMOT_SetKCubePanelParams(long lSerialNum, long lJSMode, long lJSMaxStepRate, long lJSDirSense, long lPresetPos1, long lPresetPos2, long lDispBrightness);
long WINAPI PZMOT_GetKCubePanelParams(long lSerialNum, long *plJSMode, long *plJSMaxStepRate, long *plJSDirSense, long *plPresetPos1, long *plPresetPos2, long *plDispBrightness);
long WINAPI PZMOT_SetKCubeTriggerParams(long lSerialNum, long lTrigChan1, long lTrigChan2, long lTrig1Mode, long lTrig1Polarity, long lTrig2Mode, long lTrig2Polarity);
long WINAPI PZMOT_GetKCubeTriggerParams(long lSerialNum, long *plTrigChan1, long *plTrigChan2, long *plTrig1Mode, long *plTrig1Polarity, long *plTrig2Mode, long *plTrig2Polarity);
long WINAPI PZMOT_SetKCubePosTriggerParams(long lSerialNum, long lStartPosFwd, long lPosIntervalFwd, long lNumPulsesFwd, long lStartPosRev, long lPosIntervalRev, long lNumPulsesRev, long lPulseWidth, long lNumCycles);
long WINAPI PZMOT_GetKCubePosTriggerParams(long lSerialNum, long *plStartPosFwd, long *plPosIntervalFwd, long *plNumPulsesFwd, long *plStartPosRev, long *plPosIntervalRev, long *plNumPulsesRev, long *plPulseWidth, long *plNumCycles);
long WINAPI PZMOT_SetKCubeChanEnableMode(long lSerialNum, long lMode);
long WINAPI PZMOT_GetKCubeChanEnableMode(long lSerialNum, long *plMode);
long WINAPI PZMOT_SetKCubeJogParams(long lSerialNum, long lJogMode, long lJogStepSizeFwd, long lJogStepSizeRev, long lJogStepRate, long lJogStepAccn);
long WINAPI PZMOT_GetKCubeJogParams(long lSerialNum, long *plJogMode, long *plJogStepSizeFwd, long *plJogStepSizeRev, long *plJogStepRate, long *plJogStepAccn);
long WINAPI PZMOT_SetKCubeFeedbackSig(long lSerialNum, long lFBMode, long lEncoderConst);
long WINAPI PZMOT_GetKCubeFeedbackSig(long lSerialNum, long *plFBMode, long *plEncoderConst);
long WINAPI PZMOT_GetStatusBits(long lSerialNum, long *plStatusBits);
long WINAPI PZMOT_MoveHome(long lSerialNum, BOOL bWait);
long WINAPI PZMOT_MoveRelativeStepsEx(long lSerialNum, long lRelSteps, BOOL bWait);
long WINAPI PZMOT_MoveAbsoluteStepsEx(long lSerialNum, long lAbsSteps, BOOL bWait);
long WINAPI PZMOT_MoveVelocity(long lSerialNum, long lDirection);
long WINAPI PZMOT_Stop(long lSerialNum);
long WINAPI PZMOT_MoveJog(long lSerialNum, long lJogDir);
long WINAPI PZMOT_GetInMotion(long lSerialNum, BOOL *pbInMotionFlag);

#ifdef __cplusplus
}
#endif
