import "./base/Governance.spec";
import "./ValidState.spec";

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

// GOV-78 | The specified LTV is a fraction between 0 and 1 (scaled by 10,000)
invariant ltvFractionScaled(env e, address collateral) to_mathint(LTVBorrow(e, collateral)) <= CONFIG_SCALE()
    && to_mathint(LTVLiquidation(e, collateral)) <= CONFIG_SCALE();

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

// GOV-75 | Update the protocol (Euler DAO's) receiver and fee amount for the current 
//  contract MUST affect the state
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

// GOV-76 | Update the protocol (Euler DAO's) receiver and fee amount for another 
//  contract MUST NOT affect the state
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

// GOV-26 | While distributing fees, total shares MUST not changed and accumulated fees are cleared
rule feesDistributionClearAccumulatedFeesNotAffectTotalShares(env e) {

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

// GOV-79 | Collateral LTV MUST NOT be removed completely
rule collateralLTVNotRemoved(env e, method f, calldataarg args, address collateral) 
    filtered { f -> !HARNESS_METHODS(f) } {

    bool initialized = ghostLtvInitialized[collateral];

    f(e, args);

    assert(initialized => ghostLtvInitialized[collateral]);
}
    
// GOV-41 | Initial liquidation LTV is always the previous liquidation LTV or greater 
//  than liquidation LTV when ramping
rule initialLiquidationLTVSolvency(env e, method f, calldataarg args, address collateral) 
    filtered { f -> !HARNESS_METHODS(f) && f.selector != sig:clearLTV(address).selector } {

    require(e.block.timestamp > 0);
    requireInvariant LTVTimestampFutureRamping(e, collateral);
    requireInvariant LTVTimestampValid(e, collateral);

    mathint liquidationLTVPrev = ghostLiquidationLTV[collateral];

    f(e, args);

    assert(ghostInitialLiquidationLTV[collateral] == liquidationLTVPrev
        || ghostInitialLiquidationLTV[collateral] >= ghostLiquidationLTV[collateral]
    );
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

// GOV-43 | Liquidation LTV is calculated dynamically only when ramping is in progress and always 
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

// GOV-45 | When ramping is in progress, the time remaining is always less than or equal to 
//  the ramp duration
invariant LTVRampingTimeWithinBounds(env e, address collateral) 
    to_mathint(e.block.timestamp) < ghostLtvTargetTimestamp[collateral]
        => (ghostLtvTargetTimestamp[collateral] - to_mathint(e.block.timestamp) 
            < ghostLtvRampDuration[collateral]
            )
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved with (env eFunc) {
            requireValidTimeStamp(e, eFunc);
        } 
    }

