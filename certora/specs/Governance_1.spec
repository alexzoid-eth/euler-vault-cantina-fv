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

// Initial liquidation LTV is always the previous liquidation LTV or greater than liquidation LTV when ramping
rule initialLiquidationLTVSolvency(env e, method f, calldataarg args, address collateral) 
    filtered { f -> !HARNESS_METHODS(f) } {

    require(e.block.timestamp > 0);
    requireInvariant LTVTimestampFutureRamping(e, collateral);
    requireInvariant LTVTimestampValid(e, collateral);

    mathint liquidationLTVPrev = ghostLiquidationLTV[collateral];

    f(e, args);

    assert(ghostLtvTargetTimestamp[collateral] != 0
        => ghostInitialLiquidationLTV[collateral] == liquidationLTVPrev
            || ghostInitialLiquidationLTV[collateral] >= ghostLiquidationLTV[collateral]
    );
}

// GOV-01 | Only the governor can invoke methods that modify the configuration of the vault
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

// GOV73 | Non-governor methods MUST be accessible to any callers
rule governorOnlyNotAffectOtherMethods(env e, method f, calldataarg args) 
    filtered { f -> !GOVERNOR_ONLY_METHODS(f) && !HARNESS_METHODS(f) } {

    // In this case EVCAuthenticateGovernor() in governorOnly() modifier returns msg.sender
    require(!isSenderGovernor(e));

    f@withrevert(e, args);
    bool reverted = lastReverted;

    // Other methods can be executed when sender is not a governor
    satisfy(!reverted);
}

// GOV-02 | Only one governor can exist at one time
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

// GOV-20 | Governor's ownership can be transferred
rule ownershipCanBeTransferred(env e, address newGovernorAdmin) {

    address before = governorAdmin();
    
    setGovernorAdmin(e, newGovernorAdmin);

    address after = governorAdmin();

    assert(after == newGovernorAdmin);
}

// GOV-21 | The ownership could be revoked by setting the governor to zero address
rule ownershipCanBeRevoked(env e, calldataarg args) {

    address before = governorAdmin();
    require(before != 0);

    setGovernorAdmin(e, args);

    address after = governorAdmin();

    satisfy(after == 0);
}