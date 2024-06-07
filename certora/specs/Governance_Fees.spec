import "methods/governor_methods.spec";

methods {
    function _.protocolFeeConfig(address vault) external => protocolFeeConfigCVL(vault) expect (address, uint16) ALL;

    // EVC functions summarize (required the same results when comparing a storage)
    function _.requireVaultStatusCheck() external => CONSTANT;
    function _.getCurrentOnBehalfOfAccount(address controllerToCheck) external => CONSTANT;
    function _.balanceTrackerHook(address account, uint256 newAccountBalance, bool forfeitRecentReward) external => CONSTANT;

    function _.logVaultStatus(GovernanceHarness.VaultCache memory a, uint256 interestRate) internal 
        => logVaultStatusCVL(interestRate) expect void;
}

definition HARNESS_METHODS(method f) returns bool = GOVERNANCE_HARNESS_METHODS(f);

definition CONFIG_SCALE() returns mathint = 10^4;
definition TIMESTAMP_3000_YEAR() returns uint48 = 32499081600;

///////////////// GHOSTS & HOOKS //////////////////

persistent ghost mapping(address => address) ghostProtocolFeeReceiver;
persistent ghost mapping(address => uint16) ghostProtocolFeeShare;
persistent ghost bool ghostProtocolFeeConfigCalled;
persistent ghost address ghostProtocolFeeRequestedVault {
    init_state axiom ghostProtocolFeeRequestedVault == currentContract;
}

//
// ltvLookup[].interestRate
//

persistent ghost mathint ghostInterestRate {
    init_state axiom ghostInterestRate == 0;
}

hook Sload uint72 val currentContract.vaultStorage.interestRate {
    require(require_uint72(ghostInterestRate) == val);
} 

hook Sstore currentContract.vaultStorage.interestRate uint72 val {
    ghostInterestRate = val;
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

//
// ltvLookup[].borrowLTV
//

persistent ghost mapping (address => mathint) ghostBorrowLTV {
    init_state axiom forall address i. ghostBorrowLTV[i] == 0;
}

hook Sload GovernanceHarness.ConfigAmount val currentContract.vaultStorage.ltvLookup[KEY address i].borrowLTV {
    require(require_uint16(ghostBorrowLTV[i]) == val);
} 

hook Sstore currentContract.vaultStorage.ltvLookup[KEY address i].borrowLTV GovernanceHarness.ConfigAmount val {
    ghostBorrowLTV[i] = val;
}

//
// ltvLookup[].liquidationLTV
//

persistent ghost mapping (address => mathint) ghostLiquidationLTV {
    init_state axiom forall address i. ghostLiquidationLTV[i] == 0;
}

persistent ghost mapping (address => mathint) ghostLiquidationLTVPrev {
    init_state axiom forall address i. ghostLiquidationLTVPrev[i] == 0;
}

hook Sload GovernanceHarness.ConfigAmount val currentContract.vaultStorage.ltvLookup[KEY address i].liquidationLTV {
    require(require_uint16(ghostLiquidationLTV[i]) == val);
} 

hook Sstore currentContract.vaultStorage.ltvLookup[KEY address i].liquidationLTV GovernanceHarness.ConfigAmount val {
    ghostLiquidationLTVPrev[i] = ghostLiquidationLTV[i];
    ghostLiquidationLTV[i] = val;
}

//
// ltvLookup[].initialLiquidationLTV
//

persistent ghost mapping (address => mathint) ghostInitialLiquidationLTV {
    init_state axiom forall address i. ghostInitialLiquidationLTV[i] == 0;
}

hook Sload GovernanceHarness.ConfigAmount val currentContract.vaultStorage.ltvLookup[KEY address i].initialLiquidationLTV {
    require(require_uint16(ghostInitialLiquidationLTV[i]) == val);
} 

hook Sstore currentContract.vaultStorage.ltvLookup[KEY address i].initialLiquidationLTV GovernanceHarness.ConfigAmount val {
    ghostInitialLiquidationLTV[i] = val;
}

//
// ltvLookup[].targetTimestamp
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
// ltvLookup[].rampDuration
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
// ltvLookup[].initialized
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

////////////////// FUNCTIONS //////////////////////

function updateVaultFeeConfigCVL(address vault) {

    address feeReceiver = ghostProtocolFeeReceiver[vault];
    uint16 protocolFeeShare = ghostProtocolFeeShare[vault];

    address newReceiver;
    uint16 newProtocolFeeShare;
    require(feeReceiver != newReceiver);
    require(protocolFeeShare != newProtocolFeeShare);

    ghostProtocolFeeReceiver[vault] = newReceiver;
    ghostProtocolFeeShare[vault] = newProtocolFeeShare;
}

function protocolFeeConfigCVL(address vault) returns (address, uint16) {
    ghostProtocolFeeConfigCalled = true;
    ghostProtocolFeeRequestedVault = vault;
    return (ghostProtocolFeeReceiver[vault], ghostProtocolFeeShare[vault]);
}

function requireValidTimeStamp(env eInv, env eFunc) {
    require(eInv.block.timestamp == eFunc.block.timestamp);
    require(eFunc.block.timestamp > 0);
    // There is a safe accumption `uint48(block.timestamp + rampDuration);` here, limit timestamp to 3000 year
    require(require_uint48(eFunc.block.timestamp) < TIMESTAMP_3000_YEAR());
}

persistent ghost mathint ghostLogVaultInterestRate;
function logVaultStatusCVL(uint256 interestRate) {
    ghostLogVaultInterestRate = interestRate;
}

///////////////// PROPERTIES //////////////////////

// GOV-22 | The fee receiver address can be changed
rule feeReceiverCanBeTransferred(env e, address newFeeReceiver) {

    address before = feeReceiver();
    
    setFeeReceiver(e, newFeeReceiver);

    address after = feeReceiver();

    assert(after == newFeeReceiver);
}

// GOV-23 | While distributing fees, external protocol config contract is used
rule protocolFeeConfigCalled(env e) {

    require(!ghostProtocolFeeConfigCalled);

    convertFees(e);

    satisfy(ghostProtocolFeeConfigCalled);
}

// @todo GOV-75 | Update the protocol (Euler DAO's) receiver and fee amount for the current contract MUST affect the state
rule protocolFeeParamsAffectState(env e) {

    // Disable hook and balance forwarder
    require(isHookNotSetConvertFees());
    require(!isBalanceAndBalanceEnabled(feeReceiver()));
    require(!isBalanceAndBalanceEnabled(ghostProtocolFeeReceiver[currentContract]));

    // Zero fee receivers balances
    require(feeReceiver() != ghostProtocolFeeReceiver[currentContract]);
    require(getBalance(feeReceiver()) == 0);
    require(getBalance(ghostProtocolFeeReceiver[currentContract]) == 0);

    // Get enough accumulated fees to not been rounded to zero while converting
    require(accumulatedFees(e) > 10^4);

    storage init = lastStorage;

    convertFees(e) at init;
    storage after1 = lastStorage;

    // Update fee params for current vault
    updateVaultFeeConfigCVL(currentContract);

    convertFees(e) at init;
    storage after2 = lastStorage;

    // Update fee params for current vault could affect the state
    assert(after1[currentContract] != after2[currentContract]);
}

// GOV-76 | Update the protocol (Euler DAO's) receiver and fee amount for another contract MUST NOT affect the state
rule protocolFeeParamsOfAnotherVaultNotAffectState(env e) {

    storage init = lastStorage;

    convertFees(e) at init;
    storage after1 = lastStorage;

    // Update fee params for another vault
    address anotherVault;
    require(anotherVault != currentContract);
    updateVaultFeeConfigCVL(anotherVault);

    convertFees(e) at init;
    storage after2 = lastStorage;

    // Update fee params for another vault should not affect the state
    assert(after1[currentContract] == after2[currentContract]);
}

// GOV-77 | The governor fee receiver can be disabled
rule governorFeeReceiverCanBeDisabled(env e, address newFeeReceiver) {

    address before = feeReceiver();
    require(before != 0);

    setFeeReceiver(e, newFeeReceiver);

    satisfy(feeReceiver() == 0);
}

// GOV-24 | If the governor receiver was not set, the protocol gets all fees
rule protocolGetsAllFeesIfGovernorReceiverNotSet(env e) {

    address governor = feeReceiver();
    mathint governorBalanceBefore = getBalance(governor);

    address protocol = ghostProtocolFeeReceiver[currentContract];
    mathint protocolBalanceBefore = getBalance(protocol);

    convertFees(e);

    mathint governorBalanceAfter = getBalance(governor);
    mathint protocolBalanceAfter = getBalance(protocol);

    // Governor will not receive any shares
    assert(governor == 0 => governorBalanceBefore == governorBalanceAfter);

    // Protocol can receive shares
    satisfy(protocolBalanceBefore < protocolBalanceAfter);
}

// GOV-25 | Protocol's fee share cannot be more than the max protocol fee share (50%)
rule maxProtocolFeeShareEnforced(env e) {

    address governor = feeReceiver();
    mathint governorBalanceBefore = getBalance(governor);

    address protocol = ghostProtocolFeeReceiver[currentContract];
    mathint protocolBalanceBefore = getBalance(protocol);

    convertFees(e);

    mathint governorGotShares = getBalance(governor) - governorBalanceBefore;
    mathint protocolGotShares = getBalance(protocol) - protocolBalanceBefore;

    // Protocol MUST NOT receive more than 50% shares (1 wei rounding is exception)
    assert(governor != 0 => governorGotShares >= protocolGotShares - 1);
}

// GOV-78 | Accumulated fees MUST be less or equal total shares
invariant accumulatedFeesLETotalShares(env e) accumulatedFees(e) <= totalShares(e) 
    filtered { f -> !HARNESS_METHODS(f) }

// GOV-26 | While distributing fees, total shares MUST not changed and accumulated fees are cleared
rule feesDistributionClearAccumulatedFeesNotAffectTotalShares(env e) {

    requireInvariant accumulatedFeesLETotalShares(e);

    mathint accumulatedFeesBefore = accumulatedFees(e);
    mathint totalSharesBefore = totalShares(e);

    convertFees(e);

    mathint accumulatedFeesAfter = accumulatedFees(e);
    mathint totalSharesAfter = totalShares(e);

    assert(accumulatedFeesAfter == 0);
    assert(totalSharesAfter == totalSharesBefore);
}

// GOV-27 | While distributing fees, shares are transferred to governor and protocol fee receiver addresses
rule governorAndProtocolReceiveFees(env e) {

    address governor = feeReceiver();
    mathint governorBalanceBefore = getBalance(governor);

    address protocol = ghostProtocolFeeReceiver[currentContract];
    mathint protocolBalanceBefore = getBalance(protocol);

    convertFees(e);

    mathint governorBalanceAfter = getBalance(governor);
    mathint protocolBalanceAfter = getBalance(protocol);

    satisfy(governorBalanceAfter > governorBalanceBefore);   
    satisfy(protocolBalanceAfter > protocolBalanceBefore);     
}

// GOV-28 | Fee shares cannot be transferred to the zero address
invariant validateFeeReceiverAddress() getBalance(0) == 0
    filtered { f -> !HARNESS_METHODS(f) }

// GOV-29 | Accumulated fees only increase when some time has passed
rule feesIncreaseOverTime(env e1, env e2, method f1, method f2, calldataarg args1, calldataarg args2) 
    // Exclude view functions and `convertFees()` to reduce complexity
    filtered { f1 -> !HARNESS_METHODS(f1) && !f1.isView && f1.selector != sig:convertFees().selector, 
        f2 -> !HARNESS_METHODS(f2) && !f2.isView && f2.selector != sig:convertFees().selector } {

    require(e1.block.timestamp == e2.block.timestamp);

    mathint fees1 = accumulatedFees(e1);

    f1(e1, args1);

    mathint fees2 = accumulatedFees(e1);

    f2(e2, args2);

    mathint fees3 = accumulatedFees(e2);

    // Fees were changed in first call
    assert(fees1 != fees2 => fees3 == fees2);
}

// GOV-30 | Fees are retrieved only for the contract itself from the protocol config contract
invariant feesRetrievedForCurrentContract(env e) ghostProtocolFeeRequestedVault == currentContract
    filtered { f -> !HARNESS_METHODS(f) }

// @todo GOV-31 | The specified LTV is a fraction between 0 and 1 (scaled by 10,000)
invariant ltvFractionScaled(env e, address collateral) to_mathint(LTVBorrow(e, collateral)) <= CONFIG_SCALE()
    && to_mathint(LTVLiquidation(e, collateral)) <= CONFIG_SCALE()
    filtered { f -> !HARNESS_METHODS(f) }

// GOV-32 | Self-collateralization is not allowed
invariant noSelfCollateralization(env e) LTVBorrow(e, currentContract) == 0 
    && LTVLiquidation(e, currentContract) == 0
    filtered { f -> !HARNESS_METHODS(f) }

// GOV-33 | The borrow LTV must be lower than or equal to the liquidation LTV
invariant borrowLTVLowerOrEqualLiquidationLTV(address collateral) 
    ghostBorrowLTV[collateral] <= ghostLiquidationLTV[collateral]
    filtered { f -> !HARNESS_METHODS(f) } 

// GOV-34 | Ramp duration can be used only when lowering liquidation LTV
rule rampDurationOnlyWhenLoweringLiquidationLTV(env e, method f, calldataarg args, address collateral)
    filtered { f -> !HARNESS_METHODS(f) } {
    
    uint16 borrowLTV;
    uint16 liquidationLTV;
    uint16 initialLiquidationLTV;
    uint48 targetTimestamp;
    uint32 rampDuration;
    borrowLTV, liquidationLTV, initialLiquidationLTV, targetTimestamp, rampDuration = LTVFull(collateral);
    
    liquidationLTV = LTVLiquidation(e, collateral);

    f(e, args);

    uint16 _borrowLTV;
    uint16 _liquidationLTV;
    uint16 _initialLiquidationLTV;
    uint48 _targetTimestamp;
    uint32 _rampDuration;
    _borrowLTV, _liquidationLTV, _initialLiquidationLTV, _targetTimestamp, _rampDuration = LTVFull(collateral);
        
    assert(rampDuration != _rampDuration && _rampDuration != 0 => _liquidationLTV < liquidationLTV);
}

// GOV-35 | The LTV can be set for a collateral asset, including borrow LTV, liquidation LTV, and ramp duration
rule setLTVPossibility(env e, calldataarg args, address collateral) {

    uint16 borrowLTV;
    uint16 liquidationLTV;
    uint16 initialLiquidationLTV;
    uint48 targetTimestamp;
    uint32 rampDuration;
    borrowLTV, liquidationLTV, initialLiquidationLTV, targetTimestamp, rampDuration = LTVFull(collateral);

    setLTV(e, args);

    uint16 _borrowLTV;
    uint16 _liquidationLTV;
    uint16 _initialLiquidationLTV;
    uint48 _targetTimestamp;
    uint32 _rampDuration;
    _borrowLTV, _liquidationLTV, _initialLiquidationLTV, _targetTimestamp, _rampDuration = LTVFull(collateral);

    satisfy(borrowLTV != _borrowLTV);
    satisfy(liquidationLTV != _liquidationLTV);
    satisfy(initialLiquidationLTV != _initialLiquidationLTV);
    satisfy(targetTimestamp != _targetTimestamp);
    satisfy(rampDuration != _rampDuration);
}

// GOV-36 | All collateral entries in the vault storage LTV list MUST be unique
invariant uniqueLTVEntries() forall mathint i. forall mathint j. ghostLTVList[i] != ghostLTVList[j]
    filtered { f -> !HARNESS_METHODS(f) }

// GOV-37 | The LTV is always initialized when set
invariant initializedLTVWhenSet(env e, address collateral) 
    LTVBorrow(e, collateral) != 0 || LTVLiquidation(e, collateral) != 0 => ghostLtvInitialized[collateral]
    filtered { f -> !HARNESS_METHODS(f) }

// GOV-79 | Collateral LTV MUST NOT be removed completely
rule collateralLTVNotRemoved(env e, method f, calldataarg args, address collateral) 
    filtered { f -> !HARNESS_METHODS(f) } {

    bool initialized = ghostLtvInitialized[collateral];

    f(e, args);

    assert(initialized => ghostLtvInitialized[collateral]);
}

// GOV-38 | LTV with zero timestamp should not be initialized and vice versa
invariant zeroTimestampInitializedSolvency(env e, address collateral) 
    ghostLtvTargetTimestamp[collateral] == 0 <=> ghostLtvInitialized[collateral] == false 
    filtered { f -> !HARNESS_METHODS(f) && f.selector != sig:clearLTV(address).selector } {
        preserved with (env eFunc) {
            requireValidTimeStamp(e, eFunc);
        } 
    }

// GOV-39 | LTV's timestamp is always less than or equal to the current timestamp
invariant LTVTimestampValid(env e, address collateral) ghostLtvTargetTimestamp[collateral] == 0 
    || ghostLtvTargetTimestamp[collateral] >= require_uint48(e.block.timestamp) 
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved with (env eFunc) {
            requireValidTimeStamp(e, eFunc);
        } 
    }

// GOV-40 | LTV's timestamp MUST be in the future only when ramping set
invariant LTVTimestampFutureRamping(env e, address collateral)
    ghostLtvTargetTimestamp[collateral] > require_uint48(e.block.timestamp) 
        => ghostLtvRampDuration[collateral] >= ghostLtvTargetTimestamp[collateral] - require_uint48(e.block.timestamp) 
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved with (env eFunc) {
            requireValidTimeStamp(e, eFunc);
        } 
    }
    
// @todo GOV-41 | Initial liquidation LTV is always the previous liquidation LTV or greater than liquidation LTV when ramping
invariant initialLiquidationLTVSolvency(env e, address collateral) 
    ghostInitialLiquidationLTV[collateral] == ghostLiquidationLTVPrev[collateral]
        || ghostInitialLiquidationLTV[collateral] >= ghostLiquidationLTV[collateral]
    filtered { f -> !HARNESS_METHODS(f) && f.selector != sig:clearLTV(address).selector } {
        preserved with (env eFunc) {
            requireValidTimeStamp(e, eFunc);
            requireInvariant LTVTimestampFutureRamping(e, collateral);
            requireInvariant LTVTimestampValid(e, collateral);
        }
    }

// GOV-42 | LTV can be increased or decreased immediately
rule LTVUpdateImmediate(env e, address collateral, uint16 borrowLTV, uint16 liquidationLTV, uint32 rampDuration) {

    uint16 _liquidationLTV = LTVLiquidation(e, collateral);
    uint16 _borrowLTV = LTVBorrow(e, collateral);

    setLTV(e, collateral, borrowLTV, liquidationLTV, rampDuration);

    satisfy(rampDuration == 0
        => _liquidationLTV > liquidationLTV && _borrowLTV > borrowLTV 
        || _liquidationLTV < liquidationLTV && _borrowLTV < borrowLTV
        );
}

// @todo GOV-43 | Liquidation LTV is calculated dynamically only when ramping is in progress and always 
//  between the target liquidation LTV and the initial liquidation LTV
invariant LTVLiquidationDynamic(env e, address collateral) ghostLtvRampDuration[collateral] > 0
    ? ghostLiquidationLTV[collateral] == to_mathint(LTVLiquidation(e, collateral))
    : ghostLiquidationLTV[collateral] <= to_mathint(LTVLiquidation(e, collateral))
        && to_mathint(LTVLiquidation(e, collateral)) <= ghostInitialLiquidationLTV[collateral]
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved with (env eFunc) {
            requireValidTimeStamp(e, eFunc);
            requireInvariant LTVTimestampFutureRamping(e, collateral);
            requireInvariant LTVTimestampValid(e, collateral);
        }
    }

// GOV-44 | Initialized LTV exists in collaterals list
invariant initializedLTVInCollateralList(address collateral) 
    ghostLtvInitialized[collateral] <=> collateralExists(collateral)
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved {
            // It should not be possible to overflow uint256 list
            require(ltvListLength() < max_uint64);
        }
    }

// @todo GOV-45 | When ramping is in progress, the time remaining is always less than or equal to the ramp duration
invariant LTVRampingTimeWithinBounds(env e, address collateral) 
    require_uint48(e.block.timestamp) < ghostLtvTargetTimestamp[collateral]
        => ghostLtvTargetTimestamp[collateral] - require_uint48(e.block.timestamp) < ghostLtvRampDuration[collateral]
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved with (env eFunc) {
            requireValidTimeStamp(e, eFunc);
        } 
    }

// GOV-46 | Zero timestamp means the LTV is cleared or not set yet
invariant zeroTimestampIndicatesLTVCleared(env e, address collateral) ghostLtvTargetTimestamp[collateral] == 0
    => ghostLiquidationLTV[collateral] == 0 && ghostInitialLiquidationLTV[collateral] == 0
        && ghostLtvRampDuration[collateral] == 0 && ghostBorrowLTV[collateral] == 0
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved with (env eFunc) {
            requireValidTimeStamp(e, eFunc);
        } 
    }

// GOV-48 | Config parameters are scaled to `1e4`
invariant configParamsScaledTo1e4(address collateral) 
    ghostBorrowLTV[collateral] <= CONFIG_SCALE() && ghostLiquidationLTV[collateral] <= CONFIG_SCALE()
    && to_mathint(interestFee()) <= CONFIG_SCALE() && to_mathint(maxLiquidationDiscount()) <= CONFIG_SCALE()
    // && ghostInitialLiquidationLTV[collateral] <= CONFIG_SCALE()
    filtered { f -> !HARNESS_METHODS(f) }
