-- VectorCAST 24.sp6 (11/18/24)
-- Test Case Script
--
-- Environment    : APP_SLI_ENV
-- Unit(s) Under Test: App_SLI
--

-- Script Features
TEST.SCRIPT_FEATURE:C_DIRECT_ARRAY_INDEXING
TEST.SCRIPT_FEATURE:CPP_CLASS_OBJECT_REVISION
TEST.SCRIPT_FEATURE:MULTIPLE_UUT_SUPPORT
TEST.SCRIPT_FEATURE:REMOVED_CL_PREFIX
TEST.SCRIPT_FEATURE:MIXED_CASE_NAMES
TEST.SCRIPT_FEATURE:STATIC_HEADER_FUNCS_IN_UUTS
TEST.SCRIPT_FEATURE:VCAST_MAIN_NOT_RENAMED
--

-- Unit: App_SLI

-- Subprogram: SLI_DetectEventTrigger
-- Test Case: TC_SLI_DetectEventTrigger_UT_001
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_DetectEventTrigger
TEST.NEW
TEST.NAME:TC_SLI_DetectEventTrigger_UT_001
TEST.NOTES:
##ID##
TC_SLI_DetectEventTrigger_UT_001
##End.ID##
##Description##
This testcase is created to verify when SigMgr_Get_Var_Tmp_SLI_TX returns SignalMgr_Read_Ret_OK.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{A206A86D-1302-4ba6-9C21-F747AB04708C}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_SLI_TX.return:SignalMgr_Read_Ret_OK
TEST.EXPECTED:App_SLI.SLI_DetectEventTrigger.return:false
TEST.END

-- Test Case: TC_SLI_DetectEventTrigger_UT_002
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_DetectEventTrigger
TEST.NEW
TEST.NAME:TC_SLI_DetectEventTrigger_UT_002
TEST.NOTES:
##ID##
TC_SLI_DetectEventTrigger_UT_002
##End.ID##
##Description##
This testcase is created to verify when SigMgr_Get_Var_Tmp_SLI_TX returns SignalMgr_Read_Ret_NOK.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{A206A86D-1302-4ba6-9C21-F747AB04708C}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_SLI_TX.return:SignalMgr_Read_Ret_NOK
TEST.EXPECTED:App_SLI.SLI_DetectEventTrigger.return:false
TEST.END

-- Test Case: TC_SLI_DetectEventTrigger_UT_003
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_DetectEventTrigger
TEST.NEW
TEST.NAME:TC_SLI_DetectEventTrigger_UT_003
TEST.NOTES:
##ID##
TC_SLI_DetectEventTrigger_UT_003
##End.ID##
##Description##
This testcase is created to verify if received event priority is valid.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{A206A86D-1302-4ba6-9C21-F747AB04708C}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_SLI_TX.data[0].SLITrig1:1
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_SLI_TX.return:SignalMgr_Read_Ret_OK
TEST.EXPECTED:App_SLI.SLI_DetectEventTrigger.return:true
TEST.END

-- Test Case: TC_SLI_DetectEventTrigger_UT_004
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_DetectEventTrigger
TEST.NEW
TEST.NAME:TC_SLI_DetectEventTrigger_UT_004
TEST.NOTES:
##ID##
TC_SLI_DetectEventTrigger_UT_004
##End.ID##
##Description##
This testcase is created to verify if received event priority is not valid.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{A206A86D-1302-4ba6-9C21-F747AB04708C}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_SLI_TX.return:SignalMgr_Read_Ret_OK
TEST.EXPECTED:App_SLI.SLI_DetectEventTrigger.return:false
TEST.END

-- Test Case: TC_SLI_DetectEventTrigger_UT_005
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_DetectEventTrigger
TEST.NEW
TEST.NAME:TC_SLI_DetectEventTrigger_UT_005
TEST.NOTES:
##ID##
TC_SLI_DetectEventTrigger_UT_005
##End.ID##
##Description##
This testcase is created to verify when SigMgr_Get_Var_Tmp_SLI_TX returns SLITrig2 equals to 1u.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{A206A86D-1302-4ba6-9C21-F747AB04708C}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_SLI_TX.data[0].SLITrig2:1
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_SLI_TX.return:SignalMgr_Read_Ret_OK
TEST.EXPECTED:App_SLI.SLI_DetectEventTrigger.return:true
TEST.END

-- Test Case: TC_SLI_DetectEventTrigger_UT_006
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_DetectEventTrigger
TEST.NEW
TEST.NAME:TC_SLI_DetectEventTrigger_UT_006
TEST.NOTES:
##ID##
TC_SLI_DetectEventTrigger_UT_006
##End.ID##
##Description##
This testcase is created to verify when SLIPrevTrig2 is equal to TRUE.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{A206A86D-1302-4ba6-9C21-F747AB04708C}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_SLI_TX.return:SignalMgr_Read_Ret_OK
TEST.EXPECTED:App_SLI.SLI_DetectEventTrigger.return:false
TEST.END

-- Subprogram: SLI_Init
-- Test Case: TC_SLI_Init_UT_001
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_Init
TEST.NEW
TEST.NAME:TC_SLI_Init_UT_001
TEST.NOTES:
##ID##
TC_SLI_Init_UT_001
##End.ID##
##Description##
This testcase is created to verify the SLI data structure are initialized.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{363963D8-BE2F-4440-B9FE-B7614B07E73F}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.END

-- Subprogram: SLI_MainFunction
-- Test Case: TC_SLI_MainFunction_UT_001
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_MainFunction
TEST.NEW
TEST.NAME:TC_SLI_MainFunction_UT_001
TEST.NOTES:
##ID##
TC_SLI_MainFunction_UT_001
##End.ID##
##Description##
This testcase is created to check if SLI event is detected and enabled.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{4F134604-BA80-4c0a-B2F3-B934C42840F8}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.STUB:App_SLI.SLI_isEnabled
TEST.STUB:App_SLI.SLI_DetectEventTrigger
TEST.VALUE:App_SLI.SLI_isEnabled.return:true
TEST.VALUE:App_SLI.SLI_DetectEventTrigger.return:true
TEST.END

-- Test Case: TC_SLI_MainFunction_UT_002
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_MainFunction
TEST.NEW
TEST.NAME:TC_SLI_MainFunction_UT_002
TEST.NOTES:
##ID##
TC_SLI_MainFunction_UT_002
##End.ID##
##Description##
This testcase is created to check if SLI event is detected and enabled.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{4F134604-BA80-4c0a-B2F3-B934C42840F8}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.STUB:App_SLI.SLI_isEnabled
TEST.STUB:App_SLI.SLI_DetectEventTrigger
TEST.VALUE:App_SLI.<<GLOBAL>>.SLI_Data.SLIInternalWriteSts:SLIInternalWriteSts_Capture_In_Progress
TEST.VALUE:App_SLI.SLI_DetectEventTrigger.return:true
TEST.END

-- Test Case: TC_SLI_MainFunction_UT_003
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_MainFunction
TEST.NEW
TEST.NAME:TC_SLI_MainFunction_UT_003
TEST.NOTES:
##ID##
TC_SLI_MainFunction_UT_003
##End.ID##
##Description##
This testcase is created to check when SLI event is not enabled.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{4F134604-BA80-4c0a-B2F3-B934C42840F8}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.STUB:App_SLI.SLI_isEnabled
TEST.STUB:App_SLI.SLI_DetectEventTrigger
TEST.VALUE:App_SLI.SLI_isEnabled.return:false
TEST.VALUE:App_SLI.SLI_DetectEventTrigger.return:true
TEST.END

-- Test Case: TC_SLI_MainFunction_UT_004
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_MainFunction
TEST.NEW
TEST.NAME:TC_SLI_MainFunction_UT_004
TEST.NOTES:
##ID##
TC_SLI_MainFunction_UT_004
##End.ID##
##Description##
This testcase is created to verify when SLITrig1 event is detected.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{4F134604-BA80-4c0a-B2F3-B934C42840F8}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.STUB:App_SLI.SLI_isEnabled
TEST.STUB:App_SLI.SLI_DetectEventTrigger
TEST.VALUE:App_SLI.<<GLOBAL>>.SLITrigger:SLI_Trig1
TEST.VALUE:App_SLI.SLI_isEnabled.return:true
TEST.VALUE:App_SLI.SLI_DetectEventTrigger.return:true
TEST.VALUE:uut_prototype_stubs.EQVSN_GetVisionStateMachine.currentVisionStateMachine_pe[0]:EQ_VISION_PENDING
TEST.END

-- Test Case: TC_SLI_MainFunction_UT_005
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_MainFunction
TEST.NEW
TEST.NAME:TC_SLI_MainFunction_UT_005
TEST.NOTES:
##ID##
TC_SLI_MainFunction_UT_005
##End.ID##
##Description##
This testcase is created to verify when EQ is in running Vision state.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{4F134604-BA80-4c0a-B2F3-B934C42840F8}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.STUB:App_SLI.SLI_isEnabled
TEST.STUB:App_SLI.SLI_DetectEventTrigger
TEST.VALUE:App_SLI.<<GLOBAL>>.SLITrigger:SLI_Trig1
TEST.VALUE:App_SLI.SLI_isEnabled.return:true
TEST.VALUE:App_SLI.SLI_DetectEventTrigger.return:true
TEST.VALUE:uut_prototype_stubs.EQVSN_GetVisionStateMachine.currentVisionStateMachine_pe[0]:EQ_VISION_RUNNING
TEST.END

-- Test Case: TC_SLI_MainFunction_UT_006
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_MainFunction
TEST.NEW
TEST.NAME:TC_SLI_MainFunction_UT_006
TEST.NOTES:
##ID##
TC_SLI_MainFunction_UT_006
##End.ID##
##Description##
This testcase is created to verify when EQEDR_MultipleTriggerEvent returns ret as TRUE.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{4F134604-BA80-4c0a-B2F3-B934C42840F8}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.STUB:App_SLI.SLI_isEnabled
TEST.STUB:App_SLI.SLI_DetectEventTrigger
TEST.STUB:App_SLI.SLI_callback_edrMultipleTriggerEvent
TEST.VALUE:App_SLI.<<GLOBAL>>.SLITrigger:SLI_Trig1
TEST.VALUE:App_SLI.SLI_isEnabled.return:true
TEST.VALUE:App_SLI.SLI_DetectEventTrigger.return:true
TEST.VALUE:uut_prototype_stubs.EQEDR_MultipleTriggerEvent.return:EQEDR_RET_ERROR
TEST.VALUE:uut_prototype_stubs.EQVSN_GetVisionStateMachine.currentVisionStateMachine_pe[0]:EQ_VISION_RUNNING
TEST.END

-- Subprogram: SLI_PeriodicRunnable
-- Test Case: TC_SLI_PeriodicRunnable_UT_001
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_PeriodicRunnable
TEST.NEW
TEST.NAME:TC_SLI_PeriodicRunnable_UT_001
TEST.NOTES:
##ID##
TC_SLI_PeriodicRunnable_UT_001
##End.ID##
##Description##
This testcase is created to verify SLI_initialize is false.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{598103F9-796E-4a54-B2E8-ACF3C2F3837C}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.END

-- Test Case: TC_SLI_PeriodicRunnable_UT_002
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_PeriodicRunnable
TEST.NEW
TEST.NAME:TC_SLI_PeriodicRunnable_UT_002
TEST.NOTES:
##ID##
TC_SLI_PeriodicRunnable_UT_002
##End.ID##
##Description##
This testcase is created to verify SLI_initialize is false.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{598103F9-796E-4a54-B2E8-ACF3C2F3837C}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.END

-- Subprogram: SLI_callback_edrMultipleTriggerEvent
-- Test Case: TC_SLI_callback_edrMultipleTriggerEvent_UT_001
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_callback_edrMultipleTriggerEvent
TEST.NEW
TEST.NAME:TC_SLI_callback_edrMultipleTriggerEvent_UT_001
TEST.NOTES:
##ID##
TC_SLI_callback_edrMultipleTriggerEvent_UT_001
##End.ID##
##Description##
This testcase is created to check EQ command is not executed successfully.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{2992D5A7-DFE5-4543-A4DB-B4962206F7E7}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.END

-- Test Case: TC_SLI_callback_edrMultipleTriggerEvent_UT_002
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_callback_edrMultipleTriggerEvent
TEST.NEW
TEST.NAME:TC_SLI_callback_edrMultipleTriggerEvent_UT_002
TEST.NOTES:
##ID##
TC_SLI_callback_edrMultipleTriggerEvent_UT_002
##End.ID##
##Description##
This testcase is created to verify if SLIInternalWriteSts is updated.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{2992D5A7-DFE5-4543-A4DB-B4962206F7E7}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.VALUE:App_SLI.<<GLOBAL>>.SLI_Data.SLIInternalWriteSts:SLIInternalWriteSts_Capture_In_Progress
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.replyValid:true
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.ret:0
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.numberOfTriggerReplies:2
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies:<<malloc 2>>
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies[0]:0
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies[1]:0
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_SLI_TX.return:SignalMgr_Read_Ret_NOK
TEST.END

-- Test Case: TC_SLI_callback_edrMultipleTriggerEvent_UT_003
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_callback_edrMultipleTriggerEvent
TEST.NEW
TEST.NAME:TC_SLI_callback_edrMultipleTriggerEvent_UT_003
TEST.NOTES:
##ID##
TC_SLI_callback_edrMultipleTriggerEvent_UT_003
##End.ID##
##Description##
This testcase is created to verify when ret is equal to EQS_MESP_RET_NOK.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{2992D5A7-DFE5-4543-A4DB-B4962206F7E7}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.VALUE:App_SLI.<<GLOBAL>>.SLI_Data.SLIInternalWriteSts:SLIInternalWriteSts_Capture_In_Progress
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.replyValid:true
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.ret:1
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.numberOfTriggerReplies:2
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies:<<malloc 2>>
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies[0]:0
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies[1]:0
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_SLI_TX.return:SignalMgr_Read_Ret_NOK
TEST.END

-- Test Case: TC_SLI_callback_edrMultipleTriggerEvent_UT_004
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_callback_edrMultipleTriggerEvent
TEST.NEW
TEST.NAME:TC_SLI_callback_edrMultipleTriggerEvent_UT_004
TEST.NOTES:
##ID##
TC_SLI_callback_edrMultipleTriggerEvent_UT_004
##End.ID##
##Description##
This testcase is created to verify when numberOfTriggerReplies is not equal to SLI_NUMBER_OF_TRIG_RQST(2u).
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{2992D5A7-DFE5-4543-A4DB-B4962206F7E7}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.VALUE:App_SLI.<<GLOBAL>>.SLI_Data.SLIInternalWriteSts:SLIInternalWriteSts_Capture_In_Progress
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.replyValid:true
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.ret:0
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.numberOfTriggerReplies:1
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies:<<malloc 2>>
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies[0]:0
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies[1]:0
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_SLI_TX.return:SignalMgr_Read_Ret_NOK
TEST.END

-- Test Case: TC_SLI_callback_edrMultipleTriggerEvent_UT_005
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_callback_edrMultipleTriggerEvent
TEST.NEW
TEST.NAME:TC_SLI_callback_edrMultipleTriggerEvent_UT_005
TEST.NOTES:
##ID##
TC_SLI_callback_edrMultipleTriggerEvent_UT_005
##End.ID##
##Description##
This testcase is created to verify when triggerReplies[0u] is not equal to EQS_MESP_RET_OK.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{2992D5A7-DFE5-4543-A4DB-B4962206F7E7}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.VALUE:App_SLI.<<GLOBAL>>.SLI_Data.SLIInternalWriteSts:SLIInternalWriteSts_Capture_In_Progress
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.replyValid:true
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.ret:0
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.numberOfTriggerReplies:2
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies:<<malloc 2>>
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies[0]:1
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies[1]:0
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_SLI_TX.return:SignalMgr_Read_Ret_NOK
TEST.END

-- Test Case: TC_SLI_callback_edrMultipleTriggerEvent_UT_006
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_callback_edrMultipleTriggerEvent
TEST.NEW
TEST.NAME:TC_SLI_callback_edrMultipleTriggerEvent_UT_006
TEST.NOTES:
##ID##
TC_SLI_callback_edrMultipleTriggerEvent_UT_006
##End.ID##
##Description##
This testcase is created to verify when triggerReplies[1u] is not equal to EQS_MESP_RET_OK.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{2992D5A7-DFE5-4543-A4DB-B4962206F7E7}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.VALUE:App_SLI.<<GLOBAL>>.SLI_Data.SLIInternalWriteSts:SLIInternalWriteSts_Capture_In_Progress
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.replyValid:true
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.ret:0
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.numberOfTriggerReplies:2
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies:<<malloc 2>>
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies[0]:0
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies[1]:1
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_SLI_TX.return:SignalMgr_Read_Ret_NOK
TEST.END

-- Test Case: TC_SLI_callback_edrMultipleTriggerEvent_UT_007
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_callback_edrMultipleTriggerEvent
TEST.NEW
TEST.NAME:TC_SLI_callback_edrMultipleTriggerEvent_UT_007
TEST.NOTES:
##ID##
TC_SLI_callback_edrMultipleTriggerEvent_UT_007
##End.ID##
##Description##
This testcase is created to verify when SLIInternalWriteSts is not updated.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{2992D5A7-DFE5-4543-A4DB-B4962206F7E7}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.VALUE:App_SLI.<<GLOBAL>>.SLI_Data.SLIInternalWriteSts:SLIInternalWriteSts_No_Trigger
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.replyValid:true
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.ret:0
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.numberOfTriggerReplies:2
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies:<<malloc 2>>
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies[0]:0
TEST.VALUE:App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies[1]:0
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_SLI_TX.return:SignalMgr_Read_Ret_NOK
TEST.END

-- Subprogram: SLI_isEnabled
-- Test Case: TC_SLI_isEnabled_UT_001
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_isEnabled
TEST.NEW
TEST.NAME:TC_SLI_isEnabled_UT_001
TEST.NOTES:
##ID##
TC_SLI_isEnabled_UT_001
##End.ID##
##Description##
This testcase is created to verify if SLI feature is enabled.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{8762F4D7-3EC8-440a-8738-8F942C835964}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.return:SignalMgr_Read_Ret_OK
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_SrlDat49_Prtctd_PDU.return:SignalMgr_Read_Ret_OK
TEST.END

-- Test Case: TC_SLI_isEnabled_UT_002
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_isEnabled
TEST.NEW
TEST.NAME:TC_SLI_isEnabled_UT_002
TEST.NOTES:
##ID##
TC_SLI_isEnabled_UT_002
##End.ID##
##Description##
This testcase is created to verify if SLI feature is disabled.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{8762F4D7-3EC8-440a-8738-8F942C835964}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.return:SignalMgr_Read_Ret_OK
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_SrlDat49_Prtctd_PDU.return:SignalMgr_Read_Ret_NOK
TEST.END

-- Test Case: TC_SLI_isEnabled_UT_003
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_isEnabled
TEST.NEW
TEST.NAME:TC_SLI_isEnabled_UT_003
TEST.NOTES:
##ID##
TC_SLI_isEnabled_UT_003
##End.ID##
##Description##
This testcase is created to verify if SLI feature is enabled.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{8762F4D7-3EC8-440a-8738-8F942C835964}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.data[0].GeofenRstZonStsAvl:1
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.data[0].GeofenRstZonStsFailSecAct:0
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.data[0].GeofenRstZonStsLossComFlt:0
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.return:SignalMgr_Read_Ret_OK
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_SrlDat49_Prtctd_PDU.data[0].GeofncngRstrctdZnSts:GeofncngRstrctdZnSts_Unrestricted
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_SrlDat49_Prtctd_PDU.return:SignalMgr_Read_Ret_OK
TEST.END

-- Test Case: TC_SLI_isEnabled_UT_004
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_isEnabled
TEST.NEW
TEST.NAME:TC_SLI_isEnabled_UT_004
TEST.NOTES:
##ID##
TC_SLI_isEnabled_UT_004
##End.ID##
##Description##
This testcase is created to verify if GeofncngRstrctdZnSts_Restricted != SLI_RstZnConfig.GeofncngRstrctdZnSts is FALSE.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{8762F4D7-3EC8-440a-8738-8F942C835964}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.data[0].GeofenRstZonStsAvl:1
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.data[0].GeofenRstZonStsFailSecAct:0
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.data[0].GeofenRstZonStsLossComFlt:0
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.return:SignalMgr_Read_Ret_OK
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_SrlDat49_Prtctd_PDU.data[0].GeofncngRstrctdZnSts:GeofncngRstrctdZnSts_Restricted
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_SrlDat49_Prtctd_PDU.return:SignalMgr_Read_Ret_OK
TEST.END

-- Test Case: TC_SLI_isEnabled_UT_005
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_isEnabled
TEST.NEW
TEST.NAME:TC_SLI_isEnabled_UT_005
TEST.NOTES:
##ID##
TC_SLI_isEnabled_UT_005
##End.ID##
##Description##
This testcase is created to verify when SigMgr_Get_Var_Tmp_ASDR_TX returns GeofenRstZonStsLossComFlt as TRUE.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{8762F4D7-3EC8-440a-8738-8F942C835964}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.data[0].GeofenRstZonStsAvl:1
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.data[0].GeofenRstZonStsFailSecAct:0
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.data[0].GeofenRstZonStsLossComFlt:1
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.return:SignalMgr_Read_Ret_OK
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_SrlDat49_Prtctd_PDU.data[0].GeofncngRstrctdZnSts:GeofncngRstrctdZnSts_Unrestricted
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_SrlDat49_Prtctd_PDU.return:SignalMgr_Read_Ret_OK
TEST.END

-- Test Case: TC_SLI_isEnabled_UT_006
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_isEnabled
TEST.NEW
TEST.NAME:TC_SLI_isEnabled_UT_006
TEST.NOTES:
##ID##
TC_SLI_isEnabled_UT_006
##End.ID##
##Description##
This testcase is created to verify when SigMgr_Get_Var_Tmp_ASDR_TX returns GeofenRstZonStsAvl as FALSE.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{8762F4D7-3EC8-440a-8738-8F942C835964}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.data[0].GeofenRstZonStsAvl:0
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.data[0].GeofenRstZonStsFailSecAct:0
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.data[0].GeofenRstZonStsLossComFlt:0
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.return:SignalMgr_Read_Ret_OK
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_SrlDat49_Prtctd_PDU.data[0].GeofncngRstrctdZnSts:GeofncngRstrctdZnSts_Unrestricted
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_SrlDat49_Prtctd_PDU.return:SignalMgr_Read_Ret_OK
TEST.END

-- Test Case: TC_SLI_isEnabled_UT_007
TEST.UNIT:App_SLI
TEST.SUBPROGRAM:SLI_isEnabled
TEST.NEW
TEST.NAME:TC_SLI_isEnabled_UT_007
TEST.NOTES:
##ID##
TC_SLI_isEnabled_UT_007
##End.ID##
##Description##
This testcase is created to verify when SigMgr_Get_Var_Tmp_ASDR_TX returns GeofenRstZonStsFailSecAct as TRUE.
##End.Description##
##ReviewID##
40777978
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{8762F4D7-3EC8-440a-8738-8F942C835964}
##End.GUID##
##ASIL##
- Statement Coverage
- Branch Coverage
- MC/DC Coverage
- control flow verification
- visual inspection
##End.ASIL##
##Priority##
High
##End.Priority##
TEST.END_NOTES:
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.data[0].GeofenRstZonStsAvl:1
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.data[0].GeofenRstZonStsFailSecAct:1
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.data[0].GeofenRstZonStsLossComFlt:0
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.return:SignalMgr_Read_Ret_OK
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_SrlDat49_Prtctd_PDU.data[0].GeofncngRstrctdZnSts:GeofncngRstrctdZnSts_Unrestricted
TEST.VALUE:uut_prototype_stubs.SigMgr_Get_Var_SrlDat49_Prtctd_PDU.return:SignalMgr_Read_Ret_OK
TEST.END
