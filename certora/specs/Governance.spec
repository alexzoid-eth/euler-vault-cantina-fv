import "./base/methods/GovernanceMethods.spec";
import "./base/Base.spec";
import "./common/State.spec";
import "./common/Funcs.spec";

use builtin rule sanity;
use builtin rule msgValueInLoopRule;

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

// GOV-01 | Only the governor can invoke methods that modify the configuration of the vault
rule governorOnlyMethods(env e, method f, calldataarg args) 
    filtered { f -> GOVERNOR_ONLY_METHODS(f) } {

    bool governor = isSenderGovernor(e);

    f@withrevert(e, args);
    bool reverted = lastReverted;

    // governorOnly methods should revert when sender is not a governor
    assert(!governor => reverted);
}

// GOV-02 | Only one governor can exist at one time
rule onlyOneGovernorExists(env e1, env e2, method f, calldataarg args)
    filtered { f -> GOVERNOR_ONLY_METHODS(f) } {

    // In this case EVCAuthenticateGovernor() in governorOnly() modifier returns msg.sender
    require(e1.msg.sender != EVC());
    require(e2.msg.sender != EVC());

    // First user is governor admin, second user is another
    require(e1.msg.sender == ghostGovernorAdmin);
    require(e1.msg.sender != e2.msg.sender);

    storage init = lastStorage;

    f@withrevert(e1, args) at init;
    bool revertedGovernor = lastReverted;

    f@withrevert(e2, args) at init;
    bool reverted = lastReverted;

    // If the call with first sender was successful, than the call with another sender shound fail
    assert(!revertedGovernor => reverted);
} 

// GOV-03 | Governor's ownership can be transferred
rule ownershipCanBeTransferred(env e, address newGovernorAdmin) {

    address before = ghostGovernorAdmin;
    
    setGovernorAdmin(e, newGovernorAdmin);

    assert(ghostGovernorAdmin == newGovernorAdmin);
}

// GOV-04 | The ownership could be revoked by setting the governor to zero address
rule ownershipCanBeRevoked(env e, calldataarg args) {

    require(ghostGovernorAdmin != 0);

    setGovernorAdmin(e, args);

    satisfy(ghostGovernorAdmin == 0);
}

// GOV-05 | The fee receiver address can be changed
rule feeReceiverCanBeTransferred(env e, address newFeeReceiver) {

    address before = feeReceiver();
    
    setFeeReceiver(e, newFeeReceiver);

    address after = feeReceiver();

    assert(after == newFeeReceiver);
}

// GOV-06 | While distributing fees, external protocol config contract is used
rule protocolFeeConfigCalled(env e) {

    require(!ghostProtocolFeeConfigCalled);

    convertFees(e);

    satisfy(ghostProtocolFeeConfigCalled);
}

// GOV-07 | View functions MUST NOT be protected against reentrancy
use rule viewFunctionsNotProtectedAgainstReentrancy;

// GOV-08 | View functions don't update state
use rule viewFunctionsDontUpdateState;

// GOV-09 | The governor fee receiver can be disabled
rule governorFeeReceiverCanBeDisabled(env e, address newFeeReceiver) {

    require(ghostFeeReceiver != 0);

    setFeeReceiver(e, newFeeReceiver);

    satisfy(ghostFeeReceiver == 0);
}

// GOV-10 | If the governor receiver was not set, the protocol gets all fees
rule protocolGetsAllFeesIfGovernorReceiverNotSet(env e) {

    mathint governorBalanceBefore = ghostUsersDataBalance[ghostFeeReceiver];

    address protocol = ghostProtocolFeeReceiver[currentContract];
    mathint protocolBalanceBefore = ghostUsersDataBalance[protocol];

    convertFees(e);

    mathint governorBalanceAfter = ghostUsersDataBalance[ghostFeeReceiver];
    mathint protocolBalanceAfter = ghostUsersDataBalance[protocol];

    // Governor will not receive any shares
    assert(ghostFeeReceiver == 0 => governorBalanceBefore == governorBalanceAfter);

    // Protocol can receive shares
    satisfy(protocolBalanceBefore < protocolBalanceAfter);
}

// GOV-11 | Protocol's fee share cannot be more than the max protocol fee share (50%)
rule maxProtocolFeeShareEnforced(env e) {

    address governor = feeReceiver();
    mathint governorBalanceBefore = ghostUsersDataBalance[governor];

    address protocol = ghostProtocolFeeReceiver[currentContract];
    mathint protocolBalanceBefore = ghostUsersDataBalance[protocol];

    convertFees(e);

    mathint governorGotShares = ghostUsersDataBalance[governor] - governorBalanceBefore;
    mathint protocolGotShares = ghostUsersDataBalance[protocol] - protocolBalanceBefore;

    // Protocol MUST NOT receive more than 50% shares (1 wei rounding is exception)
    assert(governor != 0 => governorGotShares >= protocolGotShares - 1);
}

// GOV-12 | While distributing fees, total shares MUST not change and accumulated fees are cleared
rule feesDistributionClearAccumulatedFeesNotAffectTotalShares(env e) {

    mathint totalSharesBefore = ghostTotalShares;

    convertFees(e);

    mathint accumulatedFeesAfter = ghostAccumulatedFees;

    assert(accumulatedFeesAfter == 0 && ghostTotalShares == totalSharesBefore);
}

// GOV-13 | While distributing fees, shares are transferred to governor and protocol fee receiver addresses
rule governorAndProtocolReceiveFees(env e) {

    address governor = feeReceiver();
    mathint governorBalanceBefore = ghostUsersDataBalance[governor];

    address protocol = ghostProtocolFeeReceiver[currentContract];
    mathint protocolBalanceBefore = ghostUsersDataBalance[protocol];

    convertFees(e);

    mathint governorBalanceAfter = ghostUsersDataBalance[governor];
    mathint protocolBalanceAfter = ghostUsersDataBalance[protocol];

    satisfy(governorBalanceAfter > governorBalanceBefore);   
    satisfy(protocolBalanceAfter > protocolBalanceBefore);     
}

// GOV-14 | Non-governor methods MUST be accessible to any callers
rule governorOnlyNotAffectOtherMethods(env e, method f, calldataarg args) 
    filtered { f -> !GOVERNOR_ONLY_METHODS(f) && !HARNESS_METHODS(f) } {

    // In this case EVCAuthenticateGovernor() in governorOnly() modifier returns msg.sender
    bool isGovernor = isSenderGovernor(e);

    f@withrevert(e, args);
    bool reverted = lastReverted;

    // Other methods can be executed when sender is not a governor
    satisfy(!isGovernor && !reverted);
}

// GOV-15 | The LTV can be set for a collateral asset, including borrow LTV, liquidation LTV, and ramp duration
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
    
// GOV-16 | LTV can be increased or decreased immediately
rule LTVUpdateImmediate(env e, address collateral, uint16 borrowLTV, uint16 liquidationLTV, uint32 rampDuration) {

    uint16 _liquidationLTV = LTVLiquidation(e, collateral);
    uint16 _borrowLTV = LTVBorrow(e, collateral);

    setLTV(e, collateral, borrowLTV, liquidationLTV, rampDuration);

    satisfy(rampDuration == 0
        => _liquidationLTV > liquidationLTV && _borrowLTV > borrowLTV 
        || _liquidationLTV < liquidationLTV && _borrowLTV < borrowLTV
        );
}

// GOV-17 | Initial liquidation LTV is always the previous liquidation LTV or greater than liquidation LTV when ramping
rule initialLiquidationLTVSolvency(env e, method f, calldataarg args, address collateral) 
    filtered { f -> !HARNESS_METHODS(f) } {

    requireValidStateEnvCollateralCVL(e, collateral);

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

// GOV-18 | Specific functions can modify state
use rule specificFunctionsModifyState;

// GOV-19 | Possibility of modifying state
use rule modifyStatePossibility;

// GOV-20 | State change functions are protected against reentrancy
use rule stateChangeFunctionsReentrancyProtected;

// GOV-21 | Anyone can execute view functions
use rule anyoneCanExecuteViewFunctions;

// GOV-22 | Hook execution allowance
use rule hookExecutionAllowance;

// GOV-23 | Hook execution possibility
use rule hookExecutionPossibility;

// GOV-24 | Hook execution restriction
use rule hookExecutionRestriction;