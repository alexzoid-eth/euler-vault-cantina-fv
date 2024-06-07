import "base/governor_harness_methods.spec";

using ProtocolConfig as _ProtocolConfig;

methods {
    function reentrancyLocked() external returns (bool) envfree;
    function hookTarget() external returns (address) envfree;

    function protocolConfigAddress() external returns (address) envfree;
}

definition HARNESS_METHODS(method f) returns bool = GOVERNANCE_HARNESS_METHODS(f);

definition GOVERNANCE_VIEW_METHODS(method f) returns bool = 
    f.selector == sig:governorAdmin().selector
    || f.selector == sig:feeReceiver().selector
    || f.selector == sig:interestFee().selector
    || f.selector == sig:interestRateModel().selector
    || f.selector == sig:protocolConfigAddress().selector
    || f.selector == sig:protocolFeeShare().selector
    || f.selector == sig:protocolFeeReceiver().selector
    || f.selector == sig:caps().selector
    || f.selector == sig:LTVBorrow(address).selector
    || f.selector == sig:LTVLiquidation(address).selector
    || f.selector == sig:LTVFull(address).selector
    || f.selector == sig:LTVList().selector
    || f.selector == sig:maxLiquidationDiscount().selector
    || f.selector == sig:liquidationCoolOffTime().selector
    || f.selector == sig:hookConfig().selector
    || f.selector == sig:configFlags().selector
    || f.selector == sig:EVC().selector
    || f.selector == sig:unitOfAccount().selector
    || f.selector == sig:oracle().selector
    || f.selector == sig:permit2Address().selector;

// GOV-16 | Anyone can execute view functions
rule anyoneCanExecuteViewFunctions(env e1, env e2, method f, calldataarg args) 
    filtered { f -> f.isView && !HARNESS_METHODS(f) } {

    require(e1.msg.value == e2.msg.value);
    require(e1.block.timestamp == e2.block.timestamp);

    require(e1.msg.sender != e2.msg.sender);

    storage init = lastStorage;

    f@withrevert(e1, args) at init;
    bool reverted1 = lastReverted;

    f@withrevert(e2, args) at init;
    bool reverted2 = lastReverted;

    // Sender address should not affect to functions execution
    assert(reverted1 == reverted2);
} 

// GOV-17 | View functions MUST NOT be protected against reentrancy
rule viewFunctionsNotProtectedAgainstReentrancy(env e, method f, calldataarg args) 
    filtered { f -> f.isView  && !HARNESS_METHODS(f) } {

    // The hook target is allowed to bypass the RO-reentrancy lock. The hook target can either be a msg.sender
    // when the view function is inlined in the EVault.sol or the hook target should be taken from the trailing
    // data appended by the delegateToModuleView function used by useView modifier. In the latter case, it is
    // safe to consume the trailing data as we know we are inside useView because msg.sender == address(this)
    require(e.msg.sender != hookTarget());
    require(e.msg.sender != currentContract);

    require(reentrancyLocked());

    f@withrevert(e, args);

    // Function could be executed when reentrancy in locked state
    satisfy(!lastReverted);
}

// GOV-19 | View functions don't update state
rule viewFunctionsDontUpdateState(env e, method f, calldataarg args) 
    filtered { f -> GOVERNANCE_VIEW_METHODS(f) } {

    storage before = lastStorage;

    f(e, args);

    storage after = lastStorage;

    assert(before[currentContract] == after[currentContract]);
}