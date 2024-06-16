import "./base/Governance.spec";
import "./common/State.spec";

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

// GV1-01 | Only the governor can invoke methods that modify the configuration of the vault
rule governorOnlyMethods(env e, method f, calldataarg args) 
    filtered { f -> GOVERNOR_ONLY_METHODS(f) } {

    // Execute checks at the same state snapshot as external call can return different results
    storage init = lastStorage;
    bool governor = isSenderGovernor(e) at init;

    f@withrevert(e, args) at init;
    bool reverted = lastReverted;

    // governorOnly methods should revert when sender is not a governor
    assert(!governor => reverted);
}

// GV1-02 | Only one governor can exist at one time
rule onlyOneGovernorExists(env e1, env e2, method f, calldataarg args)
    filtered { f -> GOVERNOR_ONLY_METHODS(f) } {

    // In this case EVCAuthenticateGovernor() in governorOnly() modifier returns msg.sender
    require(e1.msg.sender != EVC());
    require(e2.msg.sender != EVC());

    // First user is governor admin, second user is another
    require(e1.msg.sender == governorAdmin());
    require(e1.msg.sender != e2.msg.sender);

    storage init = lastStorage;

    f@withrevert(e1, args) at init;
    bool revertedGovernor = lastReverted;

    f@withrevert(e2, args) at init;
    bool reverted = lastReverted;

    // If the call with first sender was successful, than the call with another sender shound fail
    assert(!revertedGovernor => reverted);
} 

// GV1-03 | Governor's ownership can be transferred
rule ownershipCanBeTransferred(env e, address newGovernorAdmin) {

    address before = governorAdmin();
    
    setGovernorAdmin(e, newGovernorAdmin);

    address after = governorAdmin();

    assert(after == newGovernorAdmin);
}

// GV1-04 | The ownership could be revoked by setting the governor to zero address
rule ownershipCanBeRevoked(env e, calldataarg args) {

    address before = governorAdmin();
    require(before != 0);

    setGovernorAdmin(e, args);

    address after = governorAdmin();

    satisfy(after == 0);
}

// GV1-05 | The fee receiver address can be changed
rule feeReceiverCanBeTransferred(env e, address newFeeReceiver) {

    address before = feeReceiver();
    
    setFeeReceiver(e, newFeeReceiver);

    address after = feeReceiver();

    assert(after == newFeeReceiver);
}

// GV1-06 | While distributing fees, external protocol config contract is used
rule protocolFeeConfigCalled(env e) {

    require(!ghostProtocolFeeConfigCalled);

    convertFees(e);

    satisfy(ghostProtocolFeeConfigCalled);
}

// GV1-07 | Update the protocol (Euler DAO's) receiver and fee amount for the current contract MUST affect the state
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

// GV1-08 | Update the protocol (Euler DAO's) receiver and fee amount for another contract MUST NOT affect the state
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

// GV1-09 | The governor fee receiver can be disabled
rule governorFeeReceiverCanBeDisabled(env e, address newFeeReceiver) {

    address before = feeReceiver();
    require(before != 0);

    setFeeReceiver(e, newFeeReceiver);

    satisfy(feeReceiver() == 0);
}

// GV1-10 | If the governor receiver was not set, the protocol gets all fees
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

// GV1-11 | Protocol's fee share cannot be more than the max protocol fee share (50%)
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

// GV1-12 | While distributing fees, total shares MUST not change and accumulated fees are cleared
rule feesDistributionClearAccumulatedFeesNotAffectTotalShares(env e) {

    mathint accumulatedFeesBefore = accumulatedFees(e);
    mathint totalSharesBefore = totalShares(e);

    convertFees(e);

    mathint accumulatedFeesAfter = accumulatedFees(e);
    mathint totalSharesAfter = totalShares(e);

    assert(accumulatedFeesAfter == 0);
    assert(totalSharesAfter == totalSharesBefore);
}

// GV1-13 | While distributing fees, shares are transferred to governor and protocol fee receiver addresses
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

// GV1-14 | Accumulated fees only increase when some time has passed
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

// GV1-15 | The LTV can be set for a collateral asset, including borrow LTV, liquidation LTV, and ramp duration
rule setLTVPossibility(env e, calldataarg args, address collateral) {

    uint16 borrowLTV;
    uint16 liquidationLTV;
    uint16 initialLiquidationLTV;
    uint48 targetTimestamp;
    uint32 rampDuration;
    borrowLTV, liquidationLTV, initialLiquidationLTV, targetTimestamp, rampDuration = LTVFull(e, collateral);

    setLTV(e, args);

    uint16 _borrowLTV;
    uint16 _liquidationLTV;
    uint16 _initialLiquidationLTV;
    uint48 _targetTimestamp;
    uint32 _rampDuration;
    _borrowLTV, _liquidationLTV, _initialLiquidationLTV, _targetTimestamp, _rampDuration = LTVFull(e, collateral);

    satisfy(borrowLTV != _borrowLTV);
    satisfy(liquidationLTV != _liquidationLTV);
    satisfy(initialLiquidationLTV != _initialLiquidationLTV);
    satisfy(targetTimestamp != _targetTimestamp);
    satisfy(rampDuration != _rampDuration);
}
    
// GV1-16 | LTV can be increased or decreased immediately
rule LTVUpdateImmediate(env e, address collateral, uint16 borrowLTV, uint16 liquidationLTV, uint32 rampDuration) {

    uint16 _liquidationLTV = LTVLiquidation(e, collateral);
    uint16 _borrowLTV = LTVBorrow(e, collateral);

    setLTV(e, collateral, borrowLTV, liquidationLTV, rampDuration);

    satisfy(rampDuration == 0
        => _liquidationLTV > liquidationLTV && _borrowLTV > borrowLTV 
        || _liquidationLTV < liquidationLTV && _borrowLTV < borrowLTV
        );
}

// GV1-17 | Initial liquidation LTV is always the previous liquidation LTV or greater than liquidation LTV when ramping
rule initialLiquidationLTVSolvency(env e, method f, calldataarg args, address collateral) 
    filtered { f -> !HARNESS_METHODS(f) } {

    requireValidStateCollateralCVL(e, collateral);

    mathint liquidationLTVPrev = ghostLiquidationLTV[collateral];
    mathint ltvTargetTimestampPrev = ghostLtvTargetTimestamp[collateral];

    f(e, args);

    // LTV target was changed and was not cleared
    assert(ltvTargetTimestampPrev != ghostLtvTargetTimestamp[collateral] 
        && ghostLtvTargetTimestamp[collateral] != 0
        => ghostInitialLiquidationLTV[collateral] == liquidationLTVPrev
            || ghostInitialLiquidationLTV[collateral] >= ghostLiquidationLTV[collateral]
    );
}

// GV1-18 | Non-governor methods MUST be accessible to any callers
rule governorOnlyNotAffectOtherMethods(env e, method f, calldataarg args) 
    filtered { f -> !GOVERNOR_ONLY_METHODS(f) && !HARNESS_METHODS(f) } {

    // In this case EVCAuthenticateGovernor() in governorOnly() modifier returns msg.sender
    require(!isSenderGovernor(e));

    f@withrevert(e, args);
    bool reverted = lastReverted;

    // Other methods can be executed when sender is not a governor
    satisfy(!reverted);
}
