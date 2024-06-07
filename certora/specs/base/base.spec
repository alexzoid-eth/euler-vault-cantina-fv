methods {

    function reentrancyLocked() external returns (bool) envfree;

    // EVC functions summarize
    function _.requireVaultStatusCheck() external => requireVaultStatusCheckCVL() expect void;
}

persistent ghost bool ghostRequireVaultStatusCheckCalled;
function requireVaultStatusCheckCVL() {
    ghostRequireVaultStatusCheckCalled = true;
}

rule specificFunctionsModifyState(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_METHODS(f) } {
    
    storage before = lastStorage;

    f(e, args);

    storage after = lastStorage;

    assert(before[currentContract] != after[currentContract] => MODIFY_STATE_METHODS(f));
}

rule modifyStatePossibility(env e, method f, calldataarg args) 
    filtered { f -> MODIFY_STATE_METHODS(f) } {
    
    storage before = lastStorage;

    f(e, args);

    storage after = lastStorage;

    satisfy(before[currentContract] != after[currentContract]);
}

rule specificFunctionsRequireVaultStatusCheck(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_METHODS(f) } {

    require(ghostRequireVaultStatusCheckCalled == false);

    f(e, args);
    
    assert(VAULT_STATUS_CHECK_METHODS(f) <=> ghostRequireVaultStatusCheckCalled);
}

rule stateChangeFunctionsReentrancyProtected(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_METHODS(f) } {

    bool locked = reentrancyLocked();

    storage before = lastStorage;

    f(e, args);

    storage after = lastStorage;

    assert(before[currentContract] != after[currentContract] => !locked);
}

rule notAbleReceiveNativeTokens(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_METHODS(f) } {

    f@withrevert(e, args);

    assert(e.msg.value != 0 => lastReverted);
}