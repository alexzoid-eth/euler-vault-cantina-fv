import "base/Governance_Harness_methods.spec";

methods {

    function reentrancyLocked() external returns (bool) envfree;

    // EVC functions summarize
    function _.requireVaultStatusCheck() external => requireVaultStatusCheckCVL() expect void;
}

persistent ghost bool ghostRequireVaultStatusCheckCalled;
function requireVaultStatusCheckCVL() {
    ghostRequireVaultStatusCheckCalled = true;
}

definition MODIFY_STATE_METHODS(method f) returns bool = 
    f.selector == sig:setGovernorAdmin(address).selector
    || f.selector == sig:setFeeReceiver(address).selector
    || f.selector == sig:setLTV(address,uint16,uint16,uint32).selector
    || f.selector == sig:clearLTV(address).selector
    || f.selector == sig:setMaxLiquidationDiscount(uint16).selector
    || f.selector == sig:setLiquidationCoolOffTime(uint16).selector
    || f.selector == sig:setInterestRateModel(address).selector
    || f.selector == sig:setHookConfig(address,uint32).selector
    || f.selector == sig:setConfigFlags(uint32).selector
    || f.selector == sig:setCaps(uint16,uint16).selector
    || f.selector == sig:setInterestFee(uint16).selector
    || f.selector == sig:convertFees().selector;

definition VAULT_STATUS_CHECK_METHODS(method f) returns bool = 
    f.selector == sig:convertFees().selector;

// GOV-74 | Specific functions can modify state
rule specificFunctionsModifyState(env e, method f, calldataarg args) 
    filtered { f -> !GOVERNANCE_HARNESS_METHODS(f) } {
    
    storage before = lastStorage;

    f(e, args);

    storage after = lastStorage;

    assert(before[currentContract] != after[currentContract] => MODIFY_STATE_METHODS(f));
}

// GOV-09 | Specific functions require a vault status check
rule specificFunctionsRequireVaultStatusCheck(env e, method f, calldataarg args)
    filtered { f -> !GOVERNANCE_HARNESS_METHODS(f) } {

    require(ghostRequireVaultStatusCheckCalled == false);

    f(e, args);
    
    assert(VAULT_STATUS_CHECK_METHODS(f) <=> ghostRequireVaultStatusCheckCalled);
}

// GOV-12 | State change functions are protected against reentrancy
rule stateChangeFunctionsReentrancyProtected(env e, method f, calldataarg args) 
    filtered { f -> !GOVERNANCE_HARNESS_METHODS(f) } {

    bool locked = reentrancyLocked();

    storage before = lastStorage;

    f(e, args);

    storage after = lastStorage;

    assert(before[currentContract] != after[currentContract] => !locked);
}

// GOV-13 | Functions are not able to receive native tokens
rule notAbleReceiveNativeTokens(env e, method f, calldataarg args) 
    filtered { f -> !GOVERNANCE_HARNESS_METHODS(f) } {

    f@withrevert(e, args);

    assert(e.msg.value != 0 => lastReverted);
}

