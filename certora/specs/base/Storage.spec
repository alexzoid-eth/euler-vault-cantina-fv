//
// vaultStorage.lastInterestAccumulatorUpdate
//

persistent ghost uint48 ghostLastInterestAccumulatorUpdate {
    init_state axiom ghostLastInterestAccumulatorUpdate == 0;
}

hook Sload uint48 val currentContract.vaultStorage.lastInterestAccumulatorUpdate {
    require(ghostLastInterestAccumulatorUpdate == val);
} 

hook Sstore currentContract.vaultStorage.lastInterestAccumulatorUpdate uint48 val {
    ghostLastInterestAccumulatorUpdate = val;
}

//
// vaultStorage.cash
//

persistent ghost uint112 ghostCash {
    init_state axiom ghostCash == 0;
}

hook Sload BaseHarness.Assets val currentContract.vaultStorage.cash {
    require(require_uint112(ghostCash) == val);
} 

hook Sstore currentContract.vaultStorage.cash BaseHarness.Assets val {
    ghostCash = val;
}

//
// vaultStorage.supplyCap
//

persistent ghost mathint ghostSupplyCap {
    init_state axiom ghostSupplyCap == 0;
}

hook Sload BaseHarness.AmountCap val currentContract.vaultStorage.supplyCap {
    require(require_uint16(ghostSupplyCap) == val);
} 

hook Sstore currentContract.vaultStorage.supplyCap BaseHarness.AmountCap val {
    ghostSupplyCap = val;
}

//
// vaultStorage.borrowCap
//

persistent ghost mathint ghostBorrowCap {
    init_state axiom ghostBorrowCap == 0;
}

hook Sload BaseHarness.AmountCap val currentContract.vaultStorage.borrowCap {
    require(require_uint16(ghostBorrowCap) == val);
} 

hook Sstore currentContract.vaultStorage.borrowCap BaseHarness.AmountCap val {
    ghostBorrowCap = val;
}

//
// vaultStorage.hookedOps
//

persistent ghost mathint ghostHookedOps {
    init_state axiom ghostHookedOps == 0;
}

hook Sload BaseHarness.Flags val currentContract.vaultStorage.hookedOps {
    require(require_uint32(ghostHookedOps) == val);
} 

hook Sstore currentContract.vaultStorage.hookedOps BaseHarness.Flags val {
    ghostHookedOps = val;
}

//
// vaultStorage.reentrancyLocked
//

persistent ghost bool ghostReentrancyLocked {
    init_state axiom ghostReentrancyLocked == false;
}

hook Sload bool val currentContract.vaultStorage.reentrancyLocked {
    require(ghostReentrancyLocked == val);
} 

hook Sstore currentContract.vaultStorage.reentrancyLocked bool val {
    ghostReentrancyLocked = val;
}

//
// vaultStorage.snapshotInitialized
//

persistent ghost bool ghostSnapshotInitialized {
    init_state axiom ghostSnapshotInitialized == false;
}

hook Sload bool val currentContract.vaultStorage.snapshotInitialized {
    require(ghostSnapshotInitialized == val);
} 

hook Sstore currentContract.vaultStorage.snapshotInitialized bool val {
    ghostSnapshotInitialized = val;
}

//
// vaultStorage.totalShares
//

persistent ghost mathint ghostTotalShares {
    init_state axiom ghostTotalShares == 0;
}

hook Sload BaseHarness.Shares val currentContract.vaultStorage.totalShares {
    require(require_uint112(ghostTotalShares) == val);
} 

hook Sstore currentContract.vaultStorage.totalShares BaseHarness.Shares val {
    ghostTotalShares = val;
}

//
// vaultStorage.totalBorrows
//

persistent ghost mathint ghostTotalBorrows {
    init_state axiom ghostTotalBorrows == 0;
}

hook Sload BaseHarness.Owed val currentContract.vaultStorage.totalBorrows {
    require(require_uint144(ghostTotalBorrows) == val);
} 

hook Sstore currentContract.vaultStorage.totalBorrows BaseHarness.Owed val {
    ghostTotalBorrows = val;
}

//
// vaultStorage.accumulatedFees
//

persistent ghost mathint ghostAccumulatedFees {
    init_state axiom ghostAccumulatedFees == 0;
}

hook Sload BaseHarness.Shares val currentContract.vaultStorage.accumulatedFees {
    require(require_uint112(ghostAccumulatedFees) == val);
} 

hook Sstore currentContract.vaultStorage.accumulatedFees BaseHarness.Shares val {
    ghostAccumulatedFees = val;
}

//
// vaultStorage.maxLiquidationDiscount
//

persistent ghost mathint ghostMaxLiquidationDiscount {
    init_state axiom ghostMaxLiquidationDiscount == 0;
}

hook Sload BaseHarness.ConfigAmount val currentContract.vaultStorage.maxLiquidationDiscount {
    require(require_uint16(ghostMaxLiquidationDiscount) == val);
} 

hook Sstore currentContract.vaultStorage.maxLiquidationDiscount BaseHarness.ConfigAmount val {
    ghostMaxLiquidationDiscount = val;
}

//
// vaultStorage.liquidationCoolOffTime
//

persistent ghost mathint ghostLiquidationCoolOffTime {
    init_state axiom ghostLiquidationCoolOffTime == 0;
}

hook Sload uint16 val currentContract.vaultStorage.liquidationCoolOffTime {
    require(require_uint16(ghostLiquidationCoolOffTime) == val);
} 

hook Sstore currentContract.vaultStorage.liquidationCoolOffTime uint16 val {
    ghostLiquidationCoolOffTime = val;
}

//
// vaultStorage.configFlags
//

persistent ghost mathint ghostConfigFlags {
    init_state axiom ghostConfigFlags == 0;
}

hook Sload BaseHarness.Flags val currentContract.vaultStorage.configFlags {
    require(require_uint32(ghostConfigFlags) == val);
} 

hook Sstore currentContract.vaultStorage.configFlags BaseHarness.Flags val {
    ghostConfigFlags = val;
}

//
// vaultStorage.interestAccumulator
//

persistent ghost uint256 ghostInterestAccumulator {
    init_state axiom ghostInterestAccumulator == 0;
}

hook Sload uint256 val currentContract.vaultStorage.interestAccumulator {
    require(ghostInterestAccumulator == val);
} 

hook Sstore currentContract.vaultStorage.interestAccumulator uint256 val {
    ghostInterestAccumulator = val;
}

//
// vaultStorage.interestRateModel
//

persistent ghost address ghostInterestRateModel {
    init_state axiom ghostInterestRateModel == 0;
}

hook Sload address val currentContract.vaultStorage.interestRateModel {
    require(ghostInterestRateModel == val);
} 

hook Sstore currentContract.vaultStorage.interestRateModel address val {
    ghostInterestRateModel = val;
}

//
// vaultStorage.interestFee
//

persistent ghost mathint ghostInterestFee {
    init_state axiom ghostInterestFee == 0;
}

hook Sload BaseHarness.ConfigAmount val currentContract.vaultStorage.interestFee {
    require(require_uint16(ghostInterestFee) == val);
} 

hook Sstore currentContract.vaultStorage.interestFee BaseHarness.ConfigAmount val {
    ghostInterestFee = val;
}

//
// vaultStorage.interestRate
//

persistent ghost uint72 ghostInterestRate {
    init_state axiom ghostInterestRate == 0;
}

hook Sload uint72 val currentContract.vaultStorage.interestRate {
    require(ghostInterestRate == val);
} 

hook Sstore currentContract.vaultStorage.interestRate uint72 val {
    ghostInterestRate = val;
}

//
// vaultStorage.creator
//

persistent ghost address ghostCreator {
    init_state axiom ghostCreator == 0;
}

hook Sload address val currentContract.vaultStorage.creator {
    require(ghostCreator == val);
} 

hook Sstore currentContract.vaultStorage.creator address val {
    ghostCreator = val;
}

//
// vaultStorage.governorAdmin
//

persistent ghost address ghostGovernorAdmin {
    init_state axiom ghostGovernorAdmin == 0;
}

hook Sload address val currentContract.vaultStorage.governorAdmin {
    require(ghostGovernorAdmin == val);
} 

hook Sstore currentContract.vaultStorage.governorAdmin address val {
    ghostGovernorAdmin = val;
}

//
// vaultStorage.feeReceiver
//

persistent ghost address ghostFeeReceiver {
    init_state axiom ghostFeeReceiver == 0;
}

hook Sload address val currentContract.vaultStorage.feeReceiver {
    require(ghostFeeReceiver == val);
} 

hook Sstore currentContract.vaultStorage.feeReceiver address val {
    ghostFeeReceiver = val;
}

//
// vaultStorage.hookTarget
//

persistent ghost address ghostHookTarget {
    init_state axiom ghostHookTarget == 0;
}

hook Sload address val currentContract.vaultStorage.hookTarget {
    require(ghostHookTarget == val);
} 

hook Sstore currentContract.vaultStorage.hookTarget address val {
    ghostHookTarget = val;
}

//
// vaultStorage.users[].data
//

persistent ghost mapping (address => mathint) ghostUsersData {
    init_state axiom forall address i. ghostUsersData[i] == 0;
}

hook Sload BaseHarness.PackedUserSlot val currentContract.vaultStorage.users[KEY address i].data {
    require(require_uint256(ghostUsersData[i]) == val);
} 

hook Sstore currentContract.vaultStorage.users[KEY address i].data BaseHarness.PackedUserSlot val {
    ghostUsersData[i] = val;
}

//
// vaultStorage.users[].interestAccumulator
//

persistent ghost mapping (address => mathint) ghostUsersInterestAccumulator {
    init_state axiom forall address i. ghostUsersInterestAccumulator[i] == 0;
}

hook Sload uint256 val currentContract.vaultStorage.users[KEY address i].interestAccumulator {
    require(require_uint256(ghostUsersInterestAccumulator[i]) == val);
} 

hook Sstore currentContract.vaultStorage.users[KEY address i].interestAccumulator uint256 val {
    ghostUsersInterestAccumulator[i] = val;
}

//
// vaultStorage.users[].eTokenAllowance[]
//

persistent ghost mapping (address => mapping (address => mathint)) ghostUsersETokenAllowance {
    init_state axiom forall address i. forall address j. ghostUsersETokenAllowance[i][j] == 0;
}

hook Sload uint256 val currentContract.vaultStorage.users[KEY address i].eTokenAllowance[KEY address j] {
    require(require_uint256(ghostUsersETokenAllowance[i][j]) == val);
} 

hook Sstore currentContract.vaultStorage.users[KEY address i].eTokenAllowance[KEY address j] uint256 val {
    ghostUsersETokenAllowance[i][j] = val;
}

//
// vaultStorage.ltvLookup[].borrowLTV
//

persistent ghost mapping (address => mathint) ghostBorrowLTV {
    init_state axiom forall address i. ghostBorrowLTV[i] == 0;
}

hook Sload BaseHarness.ConfigAmount val currentContract.vaultStorage.ltvLookup[KEY address i].borrowLTV {
    require(require_uint16(ghostBorrowLTV[i]) == val);
} 

hook Sstore currentContract.vaultStorage.ltvLookup[KEY address i].borrowLTV BaseHarness.ConfigAmount val {
    ghostBorrowLTV[i] = val;
}

//
// vaultStorage.ltvLookup[].liquidationLTV
//

persistent ghost mapping (address => mathint) ghostLiquidationLTV {
    init_state axiom forall address i. ghostLiquidationLTV[i] == 0;
}

persistent ghost mapping (address => mathint) ghostLiquidationLTVPrev {
    init_state axiom forall address i. ghostLiquidationLTVPrev[i] == 0;
}

hook Sload BaseHarness.ConfigAmount val currentContract.vaultStorage.ltvLookup[KEY address i].liquidationLTV {
    require(require_uint16(ghostLiquidationLTV[i]) == val);
} 

hook Sstore currentContract.vaultStorage.ltvLookup[KEY address i].liquidationLTV BaseHarness.ConfigAmount val {
    ghostLiquidationLTVPrev[i] = ghostLiquidationLTV[i];
    ghostLiquidationLTV[i] = val;
}

//
// vaultStorage.ltvLookup[].initialLiquidationLTV
//

persistent ghost mapping (address => mathint) ghostInitialLiquidationLTV {
    init_state axiom forall address i. ghostInitialLiquidationLTV[i] == 0;
}

hook Sload BaseHarness.ConfigAmount val currentContract.vaultStorage.ltvLookup[KEY address i].initialLiquidationLTV {
    require(require_uint16(ghostInitialLiquidationLTV[i]) == val);
} 

hook Sstore currentContract.vaultStorage.ltvLookup[KEY address i].initialLiquidationLTV BaseHarness.ConfigAmount val {
    ghostInitialLiquidationLTV[i] = val;
}

//
// vaultStorage.ltvLookup[].targetTimestamp
//

persistent ghost mapping (address => uint48) ghostLtvTargetTimestamp {
    init_state axiom forall address i. ghostLtvTargetTimestamp[i] == 0;
}

hook Sload uint48 val currentContract.vaultStorage.ltvLookup[KEY address i].targetTimestamp {
    require(ghostLtvTargetTimestamp[i] == val);
} 

hook Sstore currentContract.vaultStorage.ltvLookup[KEY address i].targetTimestamp uint48 val {
    ghostLtvTargetTimestamp[i] = val;
}

//
// vaultStorage.ltvLookup[].rampDuration
//

persistent ghost mapping (address => mathint) ghostLtvRampDuration {
    init_state axiom forall address i. ghostLtvRampDuration[i] == 0;
}

persistent ghost mapping (address => mathint) ghostLtvRampDurationPrev {
    init_state axiom forall address i. ghostLtvRampDurationPrev[i] == 0;
}

hook Sload uint32 val currentContract.vaultStorage.ltvLookup[KEY address i].rampDuration {
    require(require_uint32(ghostLtvRampDuration[i]) == val);
} 

hook Sstore currentContract.vaultStorage.ltvLookup[KEY address i].rampDuration uint32 val {
    ghostLtvRampDurationPrev[i] = ghostLtvRampDuration[i];
    ghostLtvRampDuration[i] = val;
}

//
// vaultStorage.ltvLookup[].initialized
//

persistent ghost mapping (address => bool) ghostLtvInitialized {
    init_state axiom forall address i. ghostLtvInitialized[i] == false;
}

hook Sload bool val currentContract.vaultStorage.ltvLookup[KEY address i].initialized {
    require(ghostLtvInitialized[i] == val);
} 

hook Sstore currentContract.vaultStorage.ltvLookup[KEY address i].initialized bool val {
    ghostLtvInitialized[i] = val;
}

//
// vaultStorage.ltvList
//

persistent ghost mapping (mathint => address) ghostLTVList {
    init_state axiom forall mathint i. forall mathint j. ghostLTVList[i] != ghostLTVList[j];
}

hook Sload address val currentContract.vaultStorage.ltvList[INDEX uint256 i] {
    require(ghostLTVList[i] == val);
} 

hook Sstore currentContract.vaultStorage.ltvList[INDEX uint256 i] address val {
    ghostLTVList[i] = val;
}