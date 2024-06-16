///////////////////// EVK /////////////////////////

//
// initialized
//

persistent ghost bool ghostInitialized {
    // Set in initialize module
    init_state axiom ghostInitialized == true;
}

hook Sload bool val currentContract.initialized {
    require(ghostInitialized == val);
} 

hook Sstore currentContract.initialized bool val {
    ghostInitialized = val;
}

//
// snapshot.cash
//

persistent ghost mathint ghostSnapshotCash {
    init_state axiom ghostSnapshotCash == 0;
    axiom ghostSnapshotCash >= 0 && ghostSnapshotCash <= max_uint112;
}

hook Sload BaseHarness.Assets val currentContract.snapshot.cash {
    require(require_uint112(ghostSnapshotCash) == val);
} 

hook Sstore currentContract.snapshot.cash BaseHarness.Assets val {
    ghostSnapshotCash = val;
}

//
// snapshot.borrows
//

persistent ghost mathint ghostSnapshotBorrows {
    init_state axiom ghostSnapshotBorrows == 0;
    axiom ghostSnapshotBorrows >= 0 && ghostSnapshotBorrows <= max_uint112;
}

hook Sload BaseHarness.Assets val currentContract.snapshot.borrows {
    require(require_uint112(ghostSnapshotBorrows) == val);
} 

hook Sstore currentContract.snapshot.borrows BaseHarness.Assets val {
    ghostSnapshotBorrows = val;
}

//
// snapshot.stamp
//

persistent ghost mathint ghostSnapshotStamp {
    // Set in initialize module
    init_state axiom ghostSnapshotStamp == 1;
    axiom ghostSnapshotStamp >= 0 && ghostSnapshotStamp <= max_uint32;
}

hook Sload uint32 val currentContract.snapshot.stamp {
    require(require_uint32(ghostSnapshotStamp) == val);
} 

hook Sstore currentContract.snapshot.stamp uint32 val {
    ghostSnapshotStamp = val;
}

//
// vaultStorage.lastInterestAccumulatorUpdate
//

persistent ghost mathint ghostLastInterestAccumulatorUpdate {
    init_state axiom ghostLastInterestAccumulatorUpdate == 0;
    axiom ghostLastInterestAccumulatorUpdate >= 0 && ghostLastInterestAccumulatorUpdate <= max_uint48;
}

hook Sload uint48 val currentContract.vaultStorage.lastInterestAccumulatorUpdate {
    require(require_uint48(ghostLastInterestAccumulatorUpdate) == val);
} 

hook Sstore currentContract.vaultStorage.lastInterestAccumulatorUpdate uint48 val {
    ghostLastInterestAccumulatorUpdate = val;
}

//
// vaultStorage.cash
//

persistent ghost mathint ghostCash {
    init_state axiom ghostCash == 0;
    axiom ghostCash >= 0 && ghostCash <= max_uint112;
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
    axiom ghostSupplyCap >= 0 && ghostSupplyCap <= max_uint16;
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
    axiom ghostBorrowCap >= 0 && ghostBorrowCap <= max_uint16;
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
    axiom ghostHookedOps >= 0 && ghostHookedOps <= max_uint32;
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
    axiom ghostTotalShares >= 0 && ghostTotalShares <= max_uint112;
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
    axiom ghostTotalBorrows >= 0 && ghostTotalBorrows <= max_uint144;
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
    axiom ghostAccumulatedFees >= 0 && ghostAccumulatedFees <= max_uint112;
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
    axiom ghostMaxLiquidationDiscount >= 0 && ghostMaxLiquidationDiscount <= max_uint16;
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
    axiom ghostLiquidationCoolOffTime >= 0 && ghostLiquidationCoolOffTime <= max_uint16;
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
    axiom ghostConfigFlags >= 0 && ghostConfigFlags <= max_uint32;
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

persistent ghost mathint ghostInterestAccumulator {
    init_state axiom ghostInterestAccumulator == 0; 
    axiom ghostInterestAccumulator >= 0 && ghostInterestAccumulator <= max_uint256;
}

hook Sload uint256 val currentContract.vaultStorage.interestAccumulator {
    require(require_uint256(ghostInterestAccumulator) == val);
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
    axiom ghostInterestFee >= 0 && ghostInterestFee <= max_uint16;
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

persistent ghost mathint ghostInterestRate {
    init_state axiom ghostInterestRate == 0;
    axiom ghostInterestRate >= 0 && ghostInterestRate <= max_uint72;
}

hook Sload uint72 val currentContract.vaultStorage.interestRate {
    require(require_uint72(ghostInterestRate) == val);
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

persistent ghost mapping (address => uint256) ghostUsersData {
    init_state axiom forall address i. ghostUsersData[i] == 0;
}

// Balance stored in first 112 bits
persistent ghost mapping (address => mathint) ghostUsersDataBalance {
    init_state axiom forall address i. ghostUsersDataBalance[i] == 0;
    axiom forall address i. ghostUsersDataBalance[i] >= 0 && ghostUsersDataBalance[i] <= max_uint112;
}

hook Sload BaseHarness.PackedUserSlot val currentContract.vaultStorage.users[KEY address i].data {
    require(ghostUsersData[i] == require_uint256(val));
    require(require_uint112(ghostUsersDataBalance[i]) == require_uint112(val));
} 

hook Sstore currentContract.vaultStorage.users[KEY address i].data BaseHarness.PackedUserSlot val {
    ghostUsersData[i] = val;
    ghostUsersDataBalance[i] = require_uint112(val);
}

//
// vaultStorage.users[].interestAccumulator
//

persistent ghost mapping (address => mathint) ghostUsersInterestAccumulator {
    init_state axiom forall address i. ghostUsersInterestAccumulator[i] == 0;
    axiom forall address i. ghostUsersInterestAccumulator[i] >= 0 && ghostUsersInterestAccumulator[i] <= max_uint256;
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

persistent ghost bool ghostAllowanceTouched;

persistent ghost mapping (address => mapping (address => mathint)) ghostUsersETokenAllowance {
    init_state axiom forall address i. forall address j. ghostUsersETokenAllowance[i][j] == 0;
    axiom forall address i. forall address j. ghostUsersETokenAllowance[i][j] >= 0 && ghostUsersETokenAllowance[i][j] <= max_uint256;
}

hook Sload uint256 val currentContract.vaultStorage.users[KEY address i].eTokenAllowance[KEY address j] {
    require(require_uint256(ghostUsersETokenAllowance[i][j]) == val);
} 

hook Sstore currentContract.vaultStorage.users[KEY address i].eTokenAllowance[KEY address j] uint256 val {
    ghostAllowanceTouched = true;
    ghostUsersETokenAllowance[i][j] = val;
}

//
// vaultStorage.ltvLookup[].borrowLTV
//

persistent ghost mapping (address => mathint) ghostBorrowLTV {
    init_state axiom forall address i. ghostBorrowLTV[i] == 0;
    axiom forall address i. ghostBorrowLTV[i] >= 0 && ghostBorrowLTV[i] <= max_uint16;
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
    axiom forall address i. ghostLiquidationLTV[i] >= 0 && ghostLiquidationLTV[i] <= max_uint16;
}

hook Sload BaseHarness.ConfigAmount val currentContract.vaultStorage.ltvLookup[KEY address i].liquidationLTV {
    require(require_uint16(ghostLiquidationLTV[i]) == val);
} 

hook Sstore currentContract.vaultStorage.ltvLookup[KEY address i].liquidationLTV BaseHarness.ConfigAmount val {
    ghostLiquidationLTV[i] = val;
}

//
// vaultStorage.ltvLookup[].initialLiquidationLTV
//

persistent ghost mapping (address => mathint) ghostInitialLiquidationLTV {
    init_state axiom forall address i. ghostInitialLiquidationLTV[i] == 0;
    axiom forall address i. ghostInitialLiquidationLTV[i] >= 0 && ghostInitialLiquidationLTV[i] <= max_uint16;
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

persistent ghost mapping (address => mathint) ghostLtvTargetTimestamp {
    init_state axiom forall address i. ghostLtvTargetTimestamp[i] == 0;
    axiom forall address i. ghostInitialLiquidationLTV[i] >= 0 && ghostInitialLiquidationLTV[i] <= max_uint48;
}

hook Sload uint48 val currentContract.vaultStorage.ltvLookup[KEY address i].targetTimestamp {
    require(require_uint48(ghostLtvTargetTimestamp[i]) == val);
} 

hook Sstore currentContract.vaultStorage.ltvLookup[KEY address i].targetTimestamp uint48 val {
    ghostLtvTargetTimestamp[i] = val;
}

//
// vaultStorage.ltvLookup[].rampDuration
//

persistent ghost mapping (address => mathint) ghostLtvRampDuration {
    init_state axiom forall address i. ghostLtvRampDuration[i] == 0;
    axiom forall address i. ghostLtvRampDuration[i] >= 0 && ghostLtvRampDuration[i] <= max_uint32;
}

hook Sload uint32 val currentContract.vaultStorage.ltvLookup[KEY address i].rampDuration {
    require(require_uint32(ghostLtvRampDuration[i]) == val);
} 

hook Sstore currentContract.vaultStorage.ltvLookup[KEY address i].rampDuration uint32 val {
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

