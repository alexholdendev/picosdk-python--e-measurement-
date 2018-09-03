#
# Copyright (C) 2014-2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the ps5000aApi.h C header
file for PicoScope 5000 Series oscilloscopes using the ps5000a driver API
functions.
"""

from ctypes import *
from picosdk.library import Library
from picosdk.constants import make_enum


class Ps5000alib(Library):
    def __init__(self):
        super(Ps5000alib, self).__init__("ps5000a")


ps5000a = Ps5000alib()

ps5000a.PS5000A_DEVICE_RESOLUTION = make_enum([
    "PS5000A_DR_8BIT",
    "PS5000A_DR_12BIT",
    "PS5000A_DR_14BIT",
    "PS5000A_DR_15BIT",
    "PS5000A_DR_16BIT",
])

ps5000a.DEFAULT_RESOLUTION = ps5000a.PS5000A_DEVICE_RESOLUTION["PS5000A_DR_8BIT"]

ps5000a.PS5000A_COUPLING = make_enum([
    'PS5000A_AC',
    'PS5000A_DC',
])

# Just use AC and DC.
ps5000a.PICO_COUPLING = {k[-2:]: v for k, v in ps5000a.PS5000A_COUPLING.items()}

# A tuple in an enum like this is 2 names for the same value.
ps5000a.PS5000A_CHANNEL = make_enum([
    "PS5000A_CHANNEL_A",
    "PS5000A_CHANNEL_B",
    "PS5000A_CHANNEL_C",
    "PS5000A_CHANNEL_D",
    ("PS5000A_EXTERNAL", "PS5000A_MAX_CHANNELS"),
    "PS5000A_TRIGGER_AUX",
    "PS5000A_MAX_TRIGGER_SOURCE",
])

# only include the normal analog channels for now:
ps5000a.PICO_CHANNEL = {k[-1]: v for k, v in ps5000a.PS5000A_CHANNEL.items() if "PS5000A_CHANNEL_" in k}


ps5000a.PS5000A_RANGE = make_enum([
    "PS5000A_10MV",
    "PS5000A_20MV",
    "PS5000A_50MV",
    "PS5000A_100MV",
    "PS5000A_200MV",
    "PS5000A_500MV",
    "PS5000A_1V",
    "PS5000A_2V",
    "PS5000A_5V",
    "PS5000A_10V",
    "PS5000A_20V",
    "PS5000A_50V",
    "PS5000A_MAX_RANGES",
])

ps5000a.PICO_VOLTAGE_RANGE = {
    v: float(k.split('_')[1][:-1]) if k[-2] != 'M' else (0.001 * float(k.split('_')[1][:-2]))
    for k, v in ps5000a.PS5000A_RANGE.items() if k != "PS5000A_MAX_RANGES"
}


doc = """ PICO_STATUS (ps5000aOpenUnit)
    (
        int16_t                   *handle,
        int8_t                    *serial,
        PS5000A_DEVICE_RESOLUTION  resolution
    ); """
ps5000a.make_symbol("_OpenUnit", "ps5000aOpenUnit", c_uint32, [c_void_p, c_char_p, c_int32], doc)

doc = """ PICO_STATUS ps5000aOpenUnitAsync
    (
        int16_t                   *status,
        int8_t                    *serial,
        PS5000A_DEVICE_RESOLUTION  resolution
    ); """
ps5000a.make_symbol("_OpenUnitAsync", "ps5000aOpenUnitAsync", c_uint32, [c_void_p, c_char_p, c_int32], doc)

doc = """ PICO_STATUS ps5000aOpenUnitProgress
    (
        int16_t *handle,
        int16_t *progressPercent,
        int16_t *complete
    ); """
ps5000a.make_symbol("_OpenUnitProgress", "ps5000aOpenUnitProgress", c_uint32, [c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps5000aGetUnitInfo
    (
        int16_t   handle,
        int8_t   *string,
        int16_t   stringLength,
        int16_t  *requiredSize,
        PICO_INFO info
    ); """
ps5000a.make_symbol("_GetUnitInfo", "ps5000aGetUnitInfo", c_uint32, [c_int16, c_char_p, c_int16, c_void_p, c_uint32],
                    doc)

doc = """ PICO_STATUS ps5000aFlashLed
    (
        int16_t handle,
        int16_t start
    ); """
ps5000a.make_symbol("_FlashLed", "ps5000aFlashLed", c_uint32, [c_int16, c_int16], doc)

doc = """ PICO_STATUS ps5000aIsLedFlashing
    (
        int16_t  handle,
        int16_t *status
    ); """
ps5000a.make_symbol("_IsLedFlashing", "ps5000aIsLedFlashing", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps5000aCloseUnit
    (
        int16_t handle
    ); """
ps5000a.make_symbol("_CloseUnit", "ps5000aCloseUnit", c_uint32, [c_int16, ], doc)

doc = """ PICO_STATUS ps5000aMemorySegments
    (
        int16_t   handle,
        uint32_t  nSegments,
        int32_t  *nMaxSamples
    ); """
ps5000a.make_symbol("_MemorySegments", "ps5000aMemorySegments", c_uint32, [c_int16, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS ps5000aSetChannel
    (
        int16_t          handle,
        PS5000a_CHANNEL  channel,
        int16_t          enabled,
        PS5000a_COUPLING type,
        PS5000a_RANGE    range,
        float            analogOffset
    ); """
ps5000a.make_symbol("_SetChannel", "ps5000aSetChannel", c_uint32,
                    [c_int16, c_int32, c_int16, c_int32, c_int32, c_float], doc)

doc = """ PICO_STATUS ps5000aSetBandwidthFilter
    (
        int16_t                    handle,
        PS5000A_CHANNEL            channel,
        PS5000A_BANDWIDTH_LIMITER  bandwidth
    ); """
ps5000a.make_symbol("_SetBandwidthFilter", "ps5000aSetBandwidthFilter", c_uint32, [c_int16, c_int32, c_int32], doc)

doc = """ PICO_STATUS ps5000aGetTimebase2
    (
        int16_t   handle,
        uint32_t  timebase,
        int32_t   noSamples,
        float    *timeIntervalNanoseconds,
        int32_t  *maxSamples,
        uint32_t  segmentIndex
    ); """
ps5000a.make_symbol("_GetTimebase", "ps5000aGetTimebase2", c_uint32,
                    [c_int16, c_uint32, c_int32, c_void_p, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS ps5000aSetSigGenArbitrary
    (
        int16_t                     handle,
        int32_t                     offsetVoltage,
        uint32_t                    pkToPk,
        uint32_t                    startDeltaPhase,
        uint32_t                    stopDeltaPhase,
        uint32_t                    deltaPhaseIncrement,
        uint32_t                    dwellCount,
        int16_t                    *arbitraryWaveform,
        int32_t                     arbitraryWaveformSize,
        PS5000A_SWEEP_TYPE          sweepType,
        PS5000A_EXTRA_OPERATIONS    operation,
        PS5000A_INDEX_MODE          indexMode,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS5000A_SIGGEN_TRIG_TYPE    triggerType,
        PS5000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
ps5000a.make_symbol("_SetSigGenArbitrary", "ps5000aSetSigGenArbitrary", c_uint32,
                    [c_int16, c_int32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_void_p, c_int32, c_int32,
                     c_int32, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16], doc)

doc = """ PICO_STATUS ps5000aSetSigGenBuiltInV2
    (
        int16_t                     handle,
        int32_t                     offsetVoltage,
        uint32_t                    pkToPk,
        PS5000A_WAVE_TYPE           waveType,
        double                      startFrequency,
        double                      stopFrequency,
        double                      increment,
        double                      dwellTime,
        PS5000A_SWEEP_TYPE          sweepType,
        PS5000A_EXTRA_OPERATIONS    operation,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS5000A_SIGGEN_TRIG_TYPE    triggerType,
        PS5000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
ps5000a.make_symbol("_SetSigGenBuiltIn", "ps5000aSetSigGenBuiltInV2", c_uint32,
                    [c_int16, c_int32, c_uint32, c_int32, c_double, c_double, c_double, c_double,
                     c_int32, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16], doc)

doc = """ PICO_STATUS ps5000aSetSigGenPropertiesArbitrary
    (
        int16_t                     handle,
        uint32_t                    startDeltaPhase,
        uint32_t                    stopDeltaPhase,
        uint32_t                    deltaPhaseIncrement,
        uint32_t                    dwellCount,
        PS5000A_SWEEP_TYPE          sweepType,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS5000A_SIGGEN_TRIG_TYPE    triggerType,
        PS5000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
ps5000a.make_symbol("_SetSigGenPropertiesArbitrary", "ps5000aSetSigGenPropertiesArbitrary", c_uint32,
                    [c_int16, c_uint32, c_uint32, c_uint32, c_uint32, c_int32, c_uint32, c_uint32, c_int32, c_int32,
                     c_int16], doc)

doc = """ PICO_STATUS ps5000aSetSigGenPropertiesBuiltIn
    (
        int16_t                     handle,
        double                      startFrequency,
        double                      stopFrequency,
        double                      increment,
        double                      dwellTime,
        PS5000A_SWEEP_TYPE          sweepType,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS5000A_SIGGEN_TRIG_TYPE    triggerType,
        PS5000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
ps5000a.make_symbol("_SetSigGenPropertiesBuiltIn", "ps5000aSetSigGenPropertiesBuiltIn", c_uint32,
                    [c_int16, c_double, c_double, c_double, c_double, c_int32, c_uint32, c_uint32, c_int32, c_int32,
                     c_int16], doc)

doc = """ PICO_STATUS ps5000aSigGenFrequencyToPhase
    (
        int16_t             handle,
        double              frequency,
        PS5000A_INDEX_MODE  indexMode,
        uint32_t            bufferLength,
        uint32_t           *phase
    ); """
ps5000a.make_symbol("_SigGenFrequencyToPhase", "ps5000aSigGenFrequencyToPhase", c_uint32,
                    [c_int16, c_double, c_int32, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS ps5000aSigGenArbitraryMinMaxValues
    (
        int16_t   handle,
        int16_t  *minArbitraryWaveformValue,
        int16_t  *maxArbitraryWaveformValue,
        uint32_t *minArbitraryWaveformSize,
        uint32_t *maxArbitraryWaveformSize
    ); """
ps5000a.make_symbol("_SigGenArbitraryMinMaxValues", "ps5000aSigGenArbitraryMinMaxValues", c_uint32,
                    [c_int16, c_void_p, c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps5000aSigGenSoftwareControl
    (
        int16_t  handle,
        int16_t  state
    ); """
ps5000a.make_symbol("_SigGenSoftwareControl", "ps5000aSigGenSoftwareControl", c_uint32, [c_int16, c_int16], doc)

doc = """ PICO_STATUS ps5000aSetEts
    (
        int16_t           handle,
        PS5000A_ETS_MODE  mode,
        int16_t           etsCycles,
        int16_t           etsInterleave,
        int32_t          *sampleTimePicoseconds
    ); """
ps5000a.make_symbol("_SetEts", "ps5000aSetEts", c_uint32, [c_int16, c_int32, c_int16, c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps5000aSetTriggerChannelProperties
    (
        int16_t                             handle,
        PS5000A_TRIGGER_CHANNEL_PROPERTIES *channelProperties,
        int16_t                             nChannelProperties,
        int16_t                             auxOutputEnable,
        int32_t                             autoTriggerMilliseconds
    ); """
ps5000a.make_symbol("_SetTriggerChannelProperties", "ps5000aSetTriggerChannelProperties", c_uint32,
                    [c_int16, c_void_p, c_int16, c_int16, c_int32], doc)

doc = """ PICO_STATUS ps5000aSetTriggerChannelConditions
    (
        int16_t                     handle,
        PS5000A_TRIGGER_CONDITIONS *conditions,
        int16_t                     nConditions
    ); """
ps5000a.make_symbol("_SetTriggerChannelConditions", "ps5000aSetTriggerChannelConditions", c_uint32,
                    [c_int16, c_void_p, c_int16], doc)

doc = """ PICO_STATUS ps5000aSetTriggerChannelDirections
    (
        int16_t                      handle,
        PS5000A_THRESHOLD_DIRECTION  channelA,
        PS5000A_THRESHOLD_DIRECTION  channelB,
        PS5000A_THRESHOLD_DIRECTION  channelC,
        PS5000A_THRESHOLD_DIRECTION  channelD,
        PS5000A_THRESHOLD_DIRECTION  ext,
        PS5000A_THRESHOLD_DIRECTION  aux
    ); """
ps5000a.make_symbol("_SetTriggerChannelDirections", "ps5000aSetTriggerChannelDirections", c_uint32,
                    [c_int16, c_int32, c_int32, c_int32, c_int32, c_int32, c_int32], doc)

doc = """ PICO_STATUS ps5000aSetSimpleTrigger
    (
        int16_t                      handle,
        int16_t                      enable,
        PS5000A_CHANNEL              source,
        int16_t                      threshold,
        PS5000A_THRESHOLD_DIRECTION  direction,
        uint32_t                     delay,
        int16_t                      autoTrigger_ms
    ); """
ps5000a.make_symbol("_SetSimpleTrigger", "ps5000aSetSimpleTrigger", c_uint32,
                    [c_int16, c_int16, c_int32, c_int16, c_int32, c_uint32, c_int16], doc)

doc = """ PICO_STATUS ps5000aSetTriggerDelay
    (
        int16_t   handle,
        uint32_t  delay
    ); """
ps5000a.make_symbol("_SetTriggerDelay", "ps5000aSetTriggerDelay", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps5000aSetPulseWidthQualifier
    (
        int16_t                      handle,
        PS5000A_PWQ_CONDITIONS      *conditions,
        int16_t                      nConditions,
        PS5000A_THRESHOLD_DIRECTION  direction,
        uint32_t                     lower,
        uint32_t                     upper,
        PS5000A_PULSE_WIDTH_TYPE     type
    ); """
ps5000a.make_symbol("_SetPulseWidthQualifier", "ps5000aSetPulseWidthQualifier", c_uint32,
                    [c_int16, c_void_p, c_int16, c_int32, c_uint32, c_uint32, c_int32], doc)

doc = """ PICO_STATUS ps5000aIsTriggerOrPulseWidthQualifierEnabled
    (
        int16_t  handle,
        int16_t *triggerEnabled,
        int16_t *pulseWidthQualifierEnabled
    ); """
ps5000a.make_symbol("_IsTriggerOrPulseWidthQualifierEnabled", "ps5000aIsTriggerOrPulseWidthQualifierEnabled", c_uint32,
                    [c_int16, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps5000aGetTriggerTimeOffset64
    (
        int16_t             handle,
        int64_t            *time,
        PS5000A_TIME_UNITS *timeUnits,
        uint32_t            segmentIndex
    ); """
ps5000a.make_symbol("_GetTriggerTimeOffset", "ps5000aGetTriggerTimeOffset64", c_uint32,
                    [c_int16, c_void_p, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS ps5000aGetValuesTriggerTimeOffsetBulk64
    (
        int16_t             handle,
        int64_t            *times,
        PS5000A_TIME_UNITS *timeUnits,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex
    ); """
ps5000a.make_symbol("_GetValuesTriggerTimeOffsetBulk", "ps5000aGetValuesTriggerTimeOffsetBulk64", c_uint32,
                    [c_int16, c_void_p, c_void_p, c_uint32, c_uint32], doc)

doc = """ PICO_STATUS ps5000aSetDataBuffers
    (
        int16_t            handle,
        PS5000A_CHANNEL    channel,
        int16_t           *bufferMax,
        int16_t           *bufferMin,
        int32_t            bufferLth,
        uint32_t           segmentIndex,
        PS5000A_RATIO_MODE mode
    ); """
ps5000a.make_symbol("_SetDataBuffers", "ps5000aSetDataBuffers", c_uint32,
                    [c_int16, c_int32, c_void_p, c_void_p, c_int32, c_uint32, c_int32], doc)

doc = """ PICO_STATUS ps5000aSetDataBuffer
    (
        int16_t            handle,
        PS5000A_CHANNEL    channel,
        int16_t           *buffer,
        int32_t            bufferLth,
        uint32_t           segmentIndex,
        PS5000A_RATIO_MODE mode
    ); """
ps5000a.make_symbol("_SetDataBuffer", "ps5000aSetDataBuffer", c_uint32,
                    [c_int16, c_int32, c_void_p, c_int32, c_uint32, c_int32], doc)

doc = """ PICO_STATUS ps5000aSetEtsTimeBuffer
    (
        int16_t  handle,
        int64_t *buffer,
        int32_t  bufferLth
    ); """
ps5000a.make_symbol("_SetEtsTimeBuffer", "ps5000aSetEtsTimeBuffer", c_uint32, [c_int16, c_void_p, c_int32], doc)

doc = """ PICO_STATUS ps5000aIsReady
    (
        int16_t  handle,
        int16_t *ready
    ); """
ps5000a.make_symbol("_IsReady", "ps5000aIsReady", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps5000aRunBlock
    (
        int16_t            handle,
        int32_t            noOfPreTriggerSamples,
        int32_t            noOfPostTriggerSamples,
        uint32_t           timebase,
        int32_t           *timeIndisposedMs,
        uint32_t           segmentIndex,
        ps5000aBlockReady  lpReady,
        void              *pParameter
    ); """
ps5000a.make_symbol("_RunBlock", "ps5000aRunBlock", c_uint32,
                    [c_int16, c_int32, c_int32, c_uint32, c_void_p, c_uint32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps5000aRunStreaming
    (
        int16_t             handle,
        uint32_t            *sampleInterval,
        PS5000A_TIME_UNITS  sampleIntervalTimeUnits,
        uint32_t            maxPreTriggerSamples,
        uint32_t            maxPostPreTriggerSamples,
        int16_t             autoStop,
        uint32_t            downSampleRatio,
        PS5000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            overviewBufferSize
    ); """
ps5000a.make_symbol("_RunStreaming", "ps5000aRunStreaming", c_uint32,
                    [c_int16, c_void_p, c_int32, c_uint32, c_uint32, c_int16, c_uint32, c_int32, c_uint32], doc)

doc = """ PICO_STATUS ps5000aGetStreamingLatestValues
    (
        int16_t                handle,
        ps5000aStreamingReady  lpPs5000aReady,
        void                  *pParameter
    ); """
ps5000a.make_symbol("_GetStreamingLatestValues", "ps5000aGetStreamingLatestValues", c_uint32,
                    [c_int16, c_void_p, c_void_p], doc)

# TODO sort out how to make a callback for a C function in ctypes!
# doc = """ void *ps5000aStreamingReady
#     (
#         int16_t   handle,
#         int32_t   noOfSamples,
#         uint32_t  startIndex,
#         int16_t   overflow,
#         uint32_t  triggerAt,
#         int16_t   triggered,
#         int16_t   autoStop,
#         void     *pParameter
#     ); """
# ps5000a.make_symbol("_StreamingReady", "ps5000aStreamingReady", c_void_p,
#                     [c_int16, c_int32, c_uint32, c_int16, c_uint32, c_int16, c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps5000aNoOfStreamingValues
    (
        int16_t   handle,
        uint32_t *noOfValues
    ); """
ps5000a.make_symbol("_NoOfStreamingValues", "ps5000aNoOfStreamingValues", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps5000aGetMaxDownSampleRatio
    (
        int16_t             handle,
        uint32_t            noOfUnaggreatedSamples,
        uint32_t           *maxDownSampleRatio,
        PS5000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex
    ); """
ps5000a.make_symbol("_GetMaxDownSampleRatio", "ps5000aGetMaxDownSampleRatio", c_uint32,
                    [c_int16, c_uint32, c_void_p, c_int32, c_uint32], doc)

doc = """ PICO_STATUS ps5000aGetValues
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS5000a_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        int16_t            *overflow
    ); """
ps5000a.make_symbol("_GetValues", "ps5000aGetValues", c_uint32,
                    [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS ps5000aGetValuesAsync
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t            noOfSamples,
        uint32_t            downSampleRatio,
        PS5000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        void               *lpDataReady,
        void               *pParameter
    ); """
ps5000a.make_symbol("_GetValuesAsync", "ps5000aGetValuesAsync", c_uint32,
                    [c_int16, c_uint32, c_uint32, c_uint32, c_int32, c_uint32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps5000aGetValuesBulk
    (
        int16_t             handle,
        uint32_t           *noOfSamples,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex,
        uint32_t            downSampleRatio,
        PS5000A_RATIO_MODE  downSampleRatioMode,
        int16_t            *overflow
    ); """
ps5000a.make_symbol("_GetValuesBulk", "ps5000aGetValuesBulk", c_uint32,
                    [c_int16, c_void_p, c_uint32, c_uint32, c_uint32, c_int32, c_void_p], doc)

doc = """ PICO_STATUS ps5000aGetValuesOverlapped
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS5000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        int16_t            *overflow
    ); """
ps5000a.make_symbol("_GetValuesOverlapped", "ps5000aGetValuesOverlapped", c_uint32,
                    [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS ps5000aGetValuesOverlappedBulk
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS5000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex,
        int16_t            *overflow
    ); """
ps5000a.make_symbol("_GetValuesOverlappedBulk", "ps5000aGetValuesOverlappedBulk", c_uint32,
                    [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS ps5000aTriggerWithinPreTriggerSamples
    (
        int16_t                             handle,
        PS5000A_TRIGGER_WITHIN_PRE_TRIGGER  state
    ); """
ps5000a.make_symbol("_TriggerWithinPreTriggerSamples", "ps5000aTriggerWithinPreTriggerSamples", c_uint32,
                    [c_int16, c_int32], doc)

doc = """ PICO_STATUS ps5000aGetTriggerInfoBulk
    (
        int16_t               handle,
        PS5000A_TRIGGER_INFO *triggerInfo,
        uint32_t              fromSegmentIndex,
        uint32_t              toSegmentIndex
    ); """
ps5000a.make_symbol("_GetTriggerInfoBulk", "ps5000aGetTriggerInfoBulk", c_uint32,
                    [c_int16, c_void_p, c_uint32, c_uint32], doc)

doc = """ PICO_STATUS ps5000aEnumerateUnits
    (
        int16_t *count,
        int8_t  *serials,
        int16_t *serialLth
    ); """
ps5000a.make_symbol("_EnumerateUnits", "ps5000aEnumerateUnits", c_uint32, [c_void_p, c_char_p, c_void_p], doc)

doc = """ PICO_STATUS ps5000aGetChannelInformation
    (
        int16_t               handle,
        PS5000A_CHANNEL_INFO  info,
        int32_t               probe,
        int32_t              *ranges,
        int32_t              *length,
        int32_t               channels
    ); """
ps5000a.make_symbol("_GetChannelInformation", "ps5000aGetChannelInformation", c_uint32,
                    [c_int16, c_int32, c_int32, c_void_p, c_void_p, c_int32], doc)

doc = """ PICO_STATUS ps5000aMaximumValue
    (
        int16_t  handle,
        int16_t *value
    ); """
ps5000a.make_symbol("_MaximumValue", "ps5000aMaximumValue", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps5000aMinimumValue
    (
        int16_t  handle,
        int16_t *value
    ); """
ps5000a.make_symbol("_MinimumValue", "ps5000aMinimumValue", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps5000aGetAnalogueOffset
    (
        int16_t           handle,
        PS5000A_RANGE     range,
        PS5000A_COUPLING  coupling,
        float            *maximumVoltage,
        float            *minimumVoltage
    ); """
ps5000a.make_symbol("_GetAnalogueOffset", "ps5000aGetAnalogueOffset", c_uint32,
                    [c_int16, c_int32, c_int32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps5000aGetMaxSegments
    (
        int16_t   handle,
        uint32_t *maxSegments
    ); """
ps5000a.make_symbol("_GetMaxSegments", "ps5000aGetMaxSegments", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps5000aChangePowerSource
    (
        int16_t     handle,
        PICO_STATUS powerState
    ); """
ps5000a.make_symbol("_ChangePowerSource", "ps5000aChangePowerSource", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps5000aCurrentPowerSource
    (
        int16_t handle
    ); """
ps5000a.make_symbol("_CurrentPowerSource", "ps5000aCurrentPowerSource", c_uint32, [c_int16, ], doc)

doc = """ PICO_STATUS ps5000aStop
    (
        int16_t  handle
    ); """
ps5000a.make_symbol("_Stop", "ps5000aStop", c_uint32, [c_int16, ], doc)

doc = """ PICO_STATUS ps5000aPingUnit
    (
        int16_t  handle
    ); """
ps5000a.make_symbol("_PingUnit", "ps5000aPingUnit", c_uint32, [c_int16, ], doc)

doc = """ PICO_STATUS ps5000aSetNoOfCaptures
    (
        int16_t   handle,
        uint32_t  nCaptures
    ); """
ps5000a.make_symbol("_SetNoOfCaptures", "ps5000aSetNoOfCaptures", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps5000aGetNoOfCaptures
    (
        int16_t   handle,
        uint32_t *nCaptures
    ); """
ps5000a.make_symbol("_GetNoOfCaptures", "ps5000aGetNoOfCaptures", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps5000aGetNoOfProcessedCaptures
    (
         int16_t   handle,
         uint32_t *nProcessedCaptures
    ); """
ps5000a.make_symbol("_GetNoOfProcessedCaptures", "ps5000aGetNoOfProcessedCaptures", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps5000aSetDeviceResolution
    (
      int16_t                    handle,
      PS5000A_DEVICE_RESOLUTION  resolution
    ); """
ps5000a.make_symbol("_SetDeviceResolution", "ps5000aSetDeviceResolution", c_uint32, [c_int16, c_int32], doc)

doc = """ PICO_STATUS ps5000aGetDeviceResolution
    (
        int16_t                    handle,
        PS5000A_DEVICE_RESOLUTION *resolution
    ); """
ps5000a.make_symbol("_GetDeviceResolution", "ps5000aGetDeviceResolution", c_uint32, [c_int16, c_void_p], doc)
