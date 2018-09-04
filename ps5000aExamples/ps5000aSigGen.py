#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
# PS5000a SIGNAL GENERATOR EXAMPLE
# This example opens a 5000a driver device, sets up the singal generator to produce a sine wave, then a a square wave
# then perform a sweep of a square wave signal

import ctypes
from picosdk.ps5000a import ps5000a as ps
import time
from picosdk.functions import assert_pico_ok


# Gives the device a handle
status = {}
chandle = ctypes.c_int16()

# Opens the device/s
status["openunit"] = ps.ps5000aOpenUnit(ctypes.byref(chandle), None, 1)


try:
    assert_pico_ok(status["openunit"])
except: # PicoNotOkError:

    powerStatus = status["openunit"]

    if powerStatus == 286:
        status["changePowerSource"] = ps.ps5000aChangePowerSource(chandle, powerStatus)
    elif powerStatus == 282:
        status["changePowerSource"] = ps.ps5000aChangePowerSource(chandle, powerStatus)
    else:
        raise

    assert_pico_ok(status["changePowerSource"])

# Generates Sine signal with a 2V pkToPk with a 10KHz frequency
# handle = chandle
# offsetVoltage = 0
# pkToPk = 2000000
# waveType = ctypes.c_int16(0) = PS5000A_SINE
# startFrequency = 10000 Hz
# stopFrequency = 10000 Hz
# increment = 0
# dwellTime = 1
# sweepType = ctypes.c_int16(1) = PS5000A_UP
# operation = 0
# shots = 0
# sweeps = 0
# triggerType = ctypes.c_int16(1) = PS5000a_SIGGEN_NONE
# triggerSource = ctypes.c_int16(1) = P5000a_SIGGEN_NONE
# extInThreshold = 1
wavetype = ctypes.c_int32(0)
sweepType = ctypes.c_int32(0)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["SetSigGenBuiltIn"] = ps.ps5000aSetSigGenBuiltInV2(chandle, 0, 2000000, wavetype, 10000, 10000, 0, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)
assert_pico_ok(status["SetSigGenBuiltIn"])


# pauses the script to show signal
time.sleep(10)

# Generates Sqaure signal with a 2V pkToPk
# handle = chandle
# offsetVoltage = -1000000
# pkToPk = 1500000
# waveType = ctypes.c_int16(1) = PS5000A_Sqaure
# startFrequency = 10000 Hz
# stopFrequency = 10000 Hz
# increment = 0
# dwellTime = 1
# sweepType = ctypes.c_int16(1) = PS5000A_UP
# operation = 0
# shots = 0
# sweeps = 0
# triggerType = ctypes.c_int16(1) = PS5000A_SIGGEN_NONE
# triggerSource = ctypes.c_int16(1) = P5000A_SIGGEN_NONE
# extInThreshold = 1
wavetype = ctypes.c_int32(1)
sweepType = ctypes.c_int32(0)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["SetSigGenBuiltIn"] = ps.ps5000aSetSigGenBuiltInV2(chandle, 0, 2000000, wavetype, 10000, 10000, 0, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)
assert_pico_ok(status["SetSigGenBuiltIn"])

# pauses the script to show signal
time.sleep(10)

# Generates sqaure signal with a up down sweep, starting at 10-100 in 5KHz increments every 1 second.
# handle = chandle
# offsetVoltage = -1000000
# pkToPk = 1500000
# waveType = ctypes.c_int16(1) = PS5000a_Square
# startFrequency = 10000 Hz
# stopFrequency = 100000 Hz
# increment = 5
# dwellTime = 1
# sweepType = ctypes.c_int16(1) = PS5000a_UP
# operation = 0
# shots = 0
# sweeps = 0
# triggerType = ctypes.c_int16(1) = PS5000a_SIGGEN_NONE
# triggerSource = ctypes.c_int16(1) = P5000a_SIGGEN_NONE
# extInThreshold = 1
wavetype = ctypes.c_int32(1)
sweepType = ctypes.c_int32(2)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["SetSigGenBuiltIn"] = ps.ps5000aSetSigGenBuiltInV2(chandle, 0, 2000000, wavetype, 10000, 100000, 5, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)
assert_pico_ok(status["SetSigGenBuiltIn"])

# pauses the script to show signal
time.sleep(36)

# Stops the scope
# Handle = chandle
status["stop"] = ps.ps5000aStop(chandle)
assert_pico_ok(status["stop"])

# Closes the unit
# Handle = chandle
status["stop"] = ps.ps5000aCloseUnit(chandle)
assert_pico_ok(status["stop"])

# Displays the staus returns
print(status)