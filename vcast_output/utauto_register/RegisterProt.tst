-- VectorCAST compatible test script
-- Test Case Script
--
-- Environment    : RegisterProt_ENV
-- Unit(s) Under Test: RegisterProt
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

-- Unit: RegisterProt

-- Subprogram: registerProt_F_UnLockProt
-- Test Case: TC_registerProt_F_UnLockProt_UT_001
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_UnLockProt
TEST.NEW
TEST.NAME:TC_registerProt_F_UnLockProt_UT_001
TEST.NOTES:
##ID##
TC_registerProt_F_UnLockProt_UT_001
##End.ID##
##Description##
Baseline skeleton test for function registerProt_F_UnLockProt.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
Parameter ProtPtr of type uint32 * requires explicit/manual VectorCAST assignment.
##End.Notes##
##GUID##
{46A917D2-6243-4558-9276-F95554FA7E8C}
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

-- Test Case: TC_registerProt_F_UnLockProt_UT_002
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_UnLockProt
TEST.NEW
TEST.NAME:TC_registerProt_F_UnLockProt_UT_002
TEST.NOTES:
##ID##
TC_registerProt_F_UnLockProt_UT_002
##End.ID##
##Description##
Targets true branch of condition MCALUTIL_PROT_STATE_INIT == ProtState.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
Parameter ProtPtr of type uint32 * requires explicit/manual VectorCAST assignment.
##End.Notes##
##GUID##
{46A917D2-6243-4558-9276-F95554FA7E8C}
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

-- Test Case: TC_registerProt_F_UnLockProt_UT_003
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_UnLockProt
TEST.NEW
TEST.NAME:TC_registerProt_F_UnLockProt_UT_003
TEST.NOTES:
##ID##
TC_registerProt_F_UnLockProt_UT_003
##End.ID##
##Description##
Targets false branch of condition MCALUTIL_PROT_STATE_INIT == ProtState.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
Parameter ProtPtr of type uint32 * requires explicit/manual VectorCAST assignment.
##End.Notes##
##GUID##
{46A917D2-6243-4558-9276-F95554FA7E8C}
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

-- Test Case: TC_registerProt_F_UnLockProt_UT_004
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_UnLockProt
TEST.NEW
TEST.NAME:TC_registerProt_F_UnLockProt_UT_004
TEST.NOTES:
##ID##
TC_registerProt_F_UnLockProt_UT_004
##End.ID##
##Description##
Targets true branch of condition MCALUTIL_PROT_STATE_RUN == ProtState.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
Parameter ProtPtr of type uint32 * requires explicit/manual VectorCAST assignment.
##End.Notes##
##GUID##
{46A917D2-6243-4558-9276-F95554FA7E8C}
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

-- Test Case: TC_registerProt_F_UnLockProt_UT_005
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_UnLockProt
TEST.NEW
TEST.NAME:TC_registerProt_F_UnLockProt_UT_005
TEST.NOTES:
##ID##
TC_registerProt_F_UnLockProt_UT_005
##End.ID##
##Description##
Targets false branch of condition MCALUTIL_PROT_STATE_RUN == ProtState.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
Parameter ProtPtr of type uint32 * requires explicit/manual VectorCAST assignment.
##End.Notes##
##GUID##
{46A917D2-6243-4558-9276-F95554FA7E8C}
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

-- Subprogram: registerProt_F_LockProt
-- Test Case: TC_registerProt_F_LockProt_UT_001
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_LockProt
TEST.NEW
TEST.NAME:TC_registerProt_F_LockProt_UT_001
TEST.NOTES:
##ID##
TC_registerProt_F_LockProt_UT_001
##End.ID##
##Description##
Baseline skeleton test for function registerProt_F_LockProt.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
Parameter ProtState of type McalUtil_ProtStateType requires explicit/manual VectorCAST assignment. Parameter ProtPtr of type uint32 * requires explicit/manual VectorCAST assignment.
##End.Notes##
##GUID##
{EAB3752E-E555-4428-84A9-FAEEDC5A6AB8}
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

-- Test Case: TC_registerProt_F_LockProt_UT_002
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_LockProt
TEST.NEW
TEST.NAME:TC_registerProt_F_LockProt_UT_002
TEST.NOTES:
##ID##
TC_registerProt_F_LockProt_UT_002
##End.ID##
##Description##
Targets true branch of condition MCALUTIL_PROT_STATE_RUN == ProtState.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
Parameter ProtState of type McalUtil_ProtStateType requires explicit/manual VectorCAST assignment. Parameter ProtPtr of type uint32 * requires explicit/manual VectorCAST assignment.
##End.Notes##
##GUID##
{EAB3752E-E555-4428-84A9-FAEEDC5A6AB8}
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

-- Test Case: TC_registerProt_F_LockProt_UT_003
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_LockProt
TEST.NEW
TEST.NAME:TC_registerProt_F_LockProt_UT_003
TEST.NOTES:
##ID##
TC_registerProt_F_LockProt_UT_003
##End.ID##
##Description##
Targets false branch of condition MCALUTIL_PROT_STATE_RUN == ProtState.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
Parameter ProtState of type McalUtil_ProtStateType requires explicit/manual VectorCAST assignment. Parameter ProtPtr of type uint32 * requires explicit/manual VectorCAST assignment.
##End.Notes##
##GUID##
{EAB3752E-E555-4428-84A9-FAEEDC5A6AB8}
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

-- Subprogram: registerProt_F_UnLockDmaRpProt
-- Test Case: TC_registerProt_F_UnLockDmaRpProt_UT_001
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_UnLockDmaRpProt
TEST.NEW
TEST.NAME:TC_registerProt_F_UnLockDmaRpProt_UT_001
TEST.NOTES:
##ID##
TC_registerProt_F_UnLockDmaRpProt_UT_001
##End.ID##
##Description##
Baseline skeleton test for function registerProt_F_UnLockDmaRpProt.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{237B5B94-1AA7-426f-B2AA-15110025774C}
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

-- Test Case: TC_registerProt_F_UnLockDmaRpProt_UT_002
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_UnLockDmaRpProt
TEST.NEW
TEST.NAME:TC_registerProt_F_UnLockDmaRpProt_UT_002
TEST.NOTES:
##ID##
TC_registerProt_F_UnLockDmaRpProt_UT_002
##End.ID##
##Description##
Targets loop_zero intent for for loop.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{237B5B94-1AA7-426f-B2AA-15110025774C}
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

-- Test Case: TC_registerProt_F_UnLockDmaRpProt_UT_003
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_UnLockDmaRpProt
TEST.NEW
TEST.NAME:TC_registerProt_F_UnLockDmaRpProt_UT_003
TEST.NOTES:
##ID##
TC_registerProt_F_UnLockDmaRpProt_UT_003
##End.ID##
##Description##
Targets loop_one intent for for loop.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{237B5B94-1AA7-426f-B2AA-15110025774C}
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

-- Test Case: TC_registerProt_F_UnLockDmaRpProt_UT_004
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_UnLockDmaRpProt
TEST.NEW
TEST.NAME:TC_registerProt_F_UnLockDmaRpProt_UT_004
TEST.NOTES:
##ID##
TC_registerProt_F_UnLockDmaRpProt_UT_004
##End.ID##
##Description##
Targets loop_many intent for for loop.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{237B5B94-1AA7-426f-B2AA-15110025774C}
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

-- Subprogram: registerProt_F_LockDmaRpProt
-- Test Case: TC_registerProt_F_LockDmaRpProt_UT_001
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_LockDmaRpProt
TEST.NEW
TEST.NAME:TC_registerProt_F_LockDmaRpProt_UT_001
TEST.NOTES:
##ID##
TC_registerProt_F_LockDmaRpProt_UT_001
##End.ID##
##Description##
Baseline skeleton test for function registerProt_F_LockDmaRpProt.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{9F0E9161-3780-4fbb-88F1-A441DE06694D}
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

-- Test Case: TC_registerProt_F_LockDmaRpProt_UT_002
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_LockDmaRpProt
TEST.NEW
TEST.NAME:TC_registerProt_F_LockDmaRpProt_UT_002
TEST.NOTES:
##ID##
TC_registerProt_F_LockDmaRpProt_UT_002
##End.ID##
##Description##
Targets loop_zero intent for for loop.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{9F0E9161-3780-4fbb-88F1-A441DE06694D}
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

-- Test Case: TC_registerProt_F_LockDmaRpProt_UT_003
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_LockDmaRpProt
TEST.NEW
TEST.NAME:TC_registerProt_F_LockDmaRpProt_UT_003
TEST.NOTES:
##ID##
TC_registerProt_F_LockDmaRpProt_UT_003
##End.ID##
##Description##
Targets loop_one intent for for loop.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{9F0E9161-3780-4fbb-88F1-A441DE06694D}
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

-- Test Case: TC_registerProt_F_LockDmaRpProt_UT_004
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_LockDmaRpProt
TEST.NEW
TEST.NAME:TC_registerProt_F_LockDmaRpProt_UT_004
TEST.NOTES:
##ID##
TC_registerProt_F_LockDmaRpProt_UT_004
##End.ID##
##Description##
Targets loop_many intent for for loop.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{9F0E9161-3780-4fbb-88F1-A441DE06694D}
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

-- Subprogram: registerProt_F_UnLockQspiProt
-- Test Case: TC_registerProt_F_UnLockQspiProt_UT_001
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_UnLockQspiProt
TEST.NEW
TEST.NAME:TC_registerProt_F_UnLockQspiProt_UT_001
TEST.NOTES:
##ID##
TC_registerProt_F_UnLockQspiProt_UT_001
##End.ID##
##Description##
Baseline skeleton test for function registerProt_F_UnLockQspiProt.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{77F7CDC8-5713-402d-928E-4915A6336CC6}
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

-- Test Case: TC_registerProt_F_UnLockQspiProt_UT_002
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_UnLockQspiProt
TEST.NEW
TEST.NAME:TC_registerProt_F_UnLockQspiProt_UT_002
TEST.NOTES:
##ID##
TC_registerProt_F_UnLockQspiProt_UT_002
##End.ID##
##Description##
Targets loop_zero intent for for loop.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{77F7CDC8-5713-402d-928E-4915A6336CC6}
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

-- Test Case: TC_registerProt_F_UnLockQspiProt_UT_003
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_UnLockQspiProt
TEST.NEW
TEST.NAME:TC_registerProt_F_UnLockQspiProt_UT_003
TEST.NOTES:
##ID##
TC_registerProt_F_UnLockQspiProt_UT_003
##End.ID##
##Description##
Targets loop_one intent for for loop.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{77F7CDC8-5713-402d-928E-4915A6336CC6}
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

-- Test Case: TC_registerProt_F_UnLockQspiProt_UT_004
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_UnLockQspiProt
TEST.NEW
TEST.NAME:TC_registerProt_F_UnLockQspiProt_UT_004
TEST.NOTES:
##ID##
TC_registerProt_F_UnLockQspiProt_UT_004
##End.ID##
##Description##
Targets loop_many intent for for loop.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{77F7CDC8-5713-402d-928E-4915A6336CC6}
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

-- Subprogram: registerProt_F_LockQspiProt
-- Test Case: TC_registerProt_F_LockQspiProt_UT_001
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_LockQspiProt
TEST.NEW
TEST.NAME:TC_registerProt_F_LockQspiProt_UT_001
TEST.NOTES:
##ID##
TC_registerProt_F_LockQspiProt_UT_001
##End.ID##
##Description##
Baseline skeleton test for function registerProt_F_LockQspiProt.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{5CD41DB5-FB72-48fb-B8D1-44487A2FB6E8}
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

-- Test Case: TC_registerProt_F_LockQspiProt_UT_002
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_LockQspiProt
TEST.NEW
TEST.NAME:TC_registerProt_F_LockQspiProt_UT_002
TEST.NOTES:
##ID##
TC_registerProt_F_LockQspiProt_UT_002
##End.ID##
##Description##
Targets loop_zero intent for for loop.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{5CD41DB5-FB72-48fb-B8D1-44487A2FB6E8}
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

-- Test Case: TC_registerProt_F_LockQspiProt_UT_003
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_LockQspiProt
TEST.NEW
TEST.NAME:TC_registerProt_F_LockQspiProt_UT_003
TEST.NOTES:
##ID##
TC_registerProt_F_LockQspiProt_UT_003
##End.ID##
##Description##
Targets loop_one intent for for loop.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{5CD41DB5-FB72-48fb-B8D1-44487A2FB6E8}
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

-- Test Case: TC_registerProt_F_LockQspiProt_UT_004
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_LockQspiProt
TEST.NEW
TEST.NAME:TC_registerProt_F_LockQspiProt_UT_004
TEST.NOTES:
##ID##
TC_registerProt_F_LockQspiProt_UT_004
##End.ID##
##Description##
Targets loop_many intent for for loop.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{5CD41DB5-FB72-48fb-B8D1-44487A2FB6E8}
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

-- Subprogram: registerProt_F_enable_v
-- Test Case: TC_registerProt_F_enable_v_UT_001
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_enable_v
TEST.NEW
TEST.NAME:TC_registerProt_F_enable_v_UT_001
TEST.NOTES:
##ID##
TC_registerProt_F_enable_v_UT_001
##End.ID##
##Description##
Baseline skeleton test for function registerProt_F_enable_v.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{1483FE8F-6430-4266-976C-A06E0B36CC67}
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

-- Test Case: TC_registerProt_F_enable_v_UT_002
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_enable_v
TEST.NEW
TEST.NAME:TC_registerProt_F_enable_v_UT_002
TEST.NOTES:
##ID##
TC_registerProt_F_enable_v_UT_002
##End.ID##
##Description##
Targets true branch of condition v_idx_u8 == 9u.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{1483FE8F-6430-4266-976C-A06E0B36CC67}
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

-- Test Case: TC_registerProt_F_enable_v_UT_003
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_enable_v
TEST.NEW
TEST.NAME:TC_registerProt_F_enable_v_UT_003
TEST.NOTES:
##ID##
TC_registerProt_F_enable_v_UT_003
##End.ID##
##Description##
Targets false branch of condition v_idx_u8 == 9u.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{1483FE8F-6430-4266-976C-A06E0B36CC67}
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

-- Test Case: TC_registerProt_F_enable_v_UT_004
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_enable_v
TEST.NEW
TEST.NAME:TC_registerProt_F_enable_v_UT_004
TEST.NOTES:
##ID##
TC_registerProt_F_enable_v_UT_004
##End.ID##
##Description##
Targets true branch of condition v_idx_u8 == 9u.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{1483FE8F-6430-4266-976C-A06E0B36CC67}
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

-- Test Case: TC_registerProt_F_enable_v_UT_005
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_enable_v
TEST.NEW
TEST.NAME:TC_registerProt_F_enable_v_UT_005
TEST.NOTES:
##ID##
TC_registerProt_F_enable_v_UT_005
##End.ID##
##Description##
Targets false branch of condition v_idx_u8 == 9u.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{1483FE8F-6430-4266-976C-A06E0B36CC67}
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

-- Test Case: TC_registerProt_F_enable_v_UT_006
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_enable_v
TEST.NEW
TEST.NAME:TC_registerProt_F_enable_v_UT_006
TEST.NOTES:
##ID##
TC_registerProt_F_enable_v_UT_006
##End.ID##
##Description##
Targets true branch of condition v_idx_u8 == 9u.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{1483FE8F-6430-4266-976C-A06E0B36CC67}
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

-- Test Case: TC_registerProt_F_enable_v_UT_007
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_enable_v
TEST.NEW
TEST.NAME:TC_registerProt_F_enable_v_UT_007
TEST.NOTES:
##ID##
TC_registerProt_F_enable_v_UT_007
##End.ID##
##Description##
Targets false branch of condition v_idx_u8 == 9u.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{1483FE8F-6430-4266-976C-A06E0B36CC67}
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

-- Test Case: TC_registerProt_F_enable_v_UT_008
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_enable_v
TEST.NEW
TEST.NAME:TC_registerProt_F_enable_v_UT_008
TEST.NOTES:
##ID##
TC_registerProt_F_enable_v_UT_008
##End.ID##
##Description##
Targets true branch of condition v_idx_u8 == 9u.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{1483FE8F-6430-4266-976C-A06E0B36CC67}
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

-- Test Case: TC_registerProt_F_enable_v_UT_009
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_enable_v
TEST.NEW
TEST.NAME:TC_registerProt_F_enable_v_UT_009
TEST.NOTES:
##ID##
TC_registerProt_F_enable_v_UT_009
##End.ID##
##Description##
Targets false branch of condition v_idx_u8 == 9u.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{1483FE8F-6430-4266-976C-A06E0B36CC67}
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

-- Test Case: TC_registerProt_F_enable_v_UT_010
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_enable_v
TEST.NEW
TEST.NAME:TC_registerProt_F_enable_v_UT_010
TEST.NOTES:
##ID##
TC_registerProt_F_enable_v_UT_010
##End.ID##
##Description##
Targets true branch of condition (v_idx_u8 == 11u) || (v_idx_u8 == 13u) || (v_idx_u8 == 14u) || (v_idx_u8 == 16u)
            || (v_idx_u8 == 17u) || (v_idx_u8 == 19u) || (v_idx_u8 == 20u).
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{1483FE8F-6430-4266-976C-A06E0B36CC67}
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

-- Test Case: TC_registerProt_F_enable_v_UT_011
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_enable_v
TEST.NEW
TEST.NAME:TC_registerProt_F_enable_v_UT_011
TEST.NOTES:
##ID##
TC_registerProt_F_enable_v_UT_011
##End.ID##
##Description##
Targets false branch of condition (v_idx_u8 == 11u) || (v_idx_u8 == 13u) || (v_idx_u8 == 14u) || (v_idx_u8 == 16u)
            || (v_idx_u8 == 17u) || (v_idx_u8 == 19u) || (v_idx_u8 == 20u).
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{1483FE8F-6430-4266-976C-A06E0B36CC67}
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

-- Test Case: TC_registerProt_F_enable_v_UT_012
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_enable_v
TEST.NEW
TEST.NAME:TC_registerProt_F_enable_v_UT_012
TEST.NOTES:
##ID##
TC_registerProt_F_enable_v_UT_012
##End.ID##
##Description##
Targets true branch of condition v_idx_u8_grp >= 4u.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{1483FE8F-6430-4266-976C-A06E0B36CC67}
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

-- Test Case: TC_registerProt_F_enable_v_UT_013
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_enable_v
TEST.NEW
TEST.NAME:TC_registerProt_F_enable_v_UT_013
TEST.NOTES:
##ID##
TC_registerProt_F_enable_v_UT_013
##End.ID##
##Description##
Targets false branch of condition v_idx_u8_grp >= 4u.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{1483FE8F-6430-4266-976C-A06E0B36CC67}
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

-- Test Case: TC_registerProt_F_enable_v_UT_014
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_enable_v
TEST.NEW
TEST.NAME:TC_registerProt_F_enable_v_UT_014
TEST.NOTES:
##ID##
TC_registerProt_F_enable_v_UT_014
##End.ID##
##Description##
Targets true branch of condition (v_idx_u8 == 11u) || (v_idx_u8 == 13u) || (v_idx_u8 == 14u) || (v_idx_u8 == 16u)
            || (v_idx_u8 == 17u) || (v_idx_u8 == 19u) || (v_idx_u8 == 20u).
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{1483FE8F-6430-4266-976C-A06E0B36CC67}
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

-- Test Case: TC_registerProt_F_enable_v_UT_015
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_enable_v
TEST.NEW
TEST.NAME:TC_registerProt_F_enable_v_UT_015
TEST.NOTES:
##ID##
TC_registerProt_F_enable_v_UT_015
##End.ID##
##Description##
Targets false branch of condition (v_idx_u8 == 11u) || (v_idx_u8 == 13u) || (v_idx_u8 == 14u) || (v_idx_u8 == 16u)
            || (v_idx_u8 == 17u) || (v_idx_u8 == 19u) || (v_idx_u8 == 20u).
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{1483FE8F-6430-4266-976C-A06E0B36CC67}
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

-- Test Case: TC_registerProt_F_enable_v_UT_016
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_enable_v
TEST.NEW
TEST.NAME:TC_registerProt_F_enable_v_UT_016
TEST.NOTES:
##ID##
TC_registerProt_F_enable_v_UT_016
##End.ID##
##Description##
Targets true branch of condition v_idx_u8_grp >= 4u.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{1483FE8F-6430-4266-976C-A06E0B36CC67}
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

-- Test Case: TC_registerProt_F_enable_v_UT_017
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_enable_v
TEST.NEW
TEST.NAME:TC_registerProt_F_enable_v_UT_017
TEST.NOTES:
##ID##
TC_registerProt_F_enable_v_UT_017
##End.ID##
##Description##
Targets false branch of condition v_idx_u8_grp >= 4u.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{1483FE8F-6430-4266-976C-A06E0B36CC67}
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

-- Test Case: TC_registerProt_F_enable_v_UT_018
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_enable_v
TEST.NEW
TEST.NAME:TC_registerProt_F_enable_v_UT_018
TEST.NOTES:
##ID##
TC_registerProt_F_enable_v_UT_018
##End.ID##
##Description##
Targets true branch of condition (v_idx_u8 == 11u) || (v_idx_u8 == 13u) || (v_idx_u8 == 14u) || (v_idx_u8 == 16u)
            || (v_idx_u8 == 17u) || (v_idx_u8 == 19u) || (v_idx_u8 == 20u).
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{1483FE8F-6430-4266-976C-A06E0B36CC67}
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

-- Test Case: TC_registerProt_F_enable_v_UT_019
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_enable_v
TEST.NEW
TEST.NAME:TC_registerProt_F_enable_v_UT_019
TEST.NOTES:
##ID##
TC_registerProt_F_enable_v_UT_019
##End.ID##
##Description##
Targets false branch of condition (v_idx_u8 == 11u) || (v_idx_u8 == 13u) || (v_idx_u8 == 14u) || (v_idx_u8 == 16u)
            || (v_idx_u8 == 17u) || (v_idx_u8 == 19u) || (v_idx_u8 == 20u).
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{1483FE8F-6430-4266-976C-A06E0B36CC67}
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

-- Test Case: TC_registerProt_F_enable_v_UT_020
TEST.UNIT:RegisterProt
TEST.SUBPROGRAM:registerProt_F_enable_v
TEST.NEW
TEST.NAME:TC_registerProt_F_enable_v_UT_020
TEST.NOTES:
##ID##
TC_registerProt_F_enable_v_UT_020
##End.ID##
##Description##
Targets true branch of condition v_idx_u8_grp >= 4u.
##End.Description##
##ReviewID##
TBD
##End.ReviewID##
##Status##
In Review
##End.Status##
##Notes##
##End.Notes##
##GUID##
{1483FE8F-6430-4266-976C-A06E0B36CC67}
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
