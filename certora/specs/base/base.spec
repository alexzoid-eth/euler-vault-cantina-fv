definition CHECKACCOUNT_NONE() returns address = 0;
definition CHECKACCOUNT_CALLER() returns address = 1;

function getCurrentOnBehalfOfAccountCVL() returns (address, bool) {
    address onBehalfOfAccount;
    bool controllerEnabled;

    require(onBehalfOfAccount != 0);

    return (onBehalfOfAccount, controllerEnabled);
}

persistent ghost bool ghostRequireVaultStatusCheckCalled;
function requireVaultStatusCheckCVL() {
    ghostRequireVaultStatusCheckCalled = true;
}

persistent ghost bool ghostRequireVaultAccountStatusCheckCalled;
function requireVaultAccountStatusCheckCVL(address caller) {
    ghostRequireVaultAccountStatusCheckCalled = true;
    assert(caller != CHECKACCOUNT_CALLER());
}

function reentrantViewSenderRequirementCVL(env e) {
    // The hook target is allowed to bypass the RO-reentrancy lock. The hook target can either be a msg.sender
    // when the view function is inlined in the EVault.sol or the hook target should be taken from the trailing
    // data appended by the delegateToModuleView function used by useView modifier. In the latter case, it is
    // safe to consume the trailing data as we know we are inside useView because msg.sender == address(this)
    require(e.msg.sender != hookTarget());
    require(e.msg.sender != currentContract);
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

rule anyoneCanExecuteViewFunctions(env e1, env e2, method f, calldataarg args) 
    filtered { f -> f.isView && !HARNESS_METHODS(f) } {

    reentrantViewSenderRequirementCVL(e1);
    reentrantViewSenderRequirementCVL(e2);

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

rule viewFunctionsNotProtectedAgainstReentrancy(env e, method f, calldataarg args) 
    filtered { f -> f.isView  && !HARNESS_METHODS(f) } {

    reentrantViewSenderRequirementCVL(e);

    require(reentrancyLocked());

    f@withrevert(e, args);

    // Function could be executed when reentrancy in locked state
    satisfy(!lastReverted);
}

rule specificViewFunctionsProtectedAgainstReentrancy(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_METHODS(f) } {

    reentrantViewSenderRequirementCVL(e);

    require(reentrancyLocked());

    f@withrevert(e, args);
    bool reverted = lastReverted;

    // MUST revert
    assert(VIEW_REENTRANCY_PROTECTED_METHODS(f) => reverted);

    // Possibility not been reverted
    satisfy(f.isView && !VIEW_REENTRANCY_PROTECTED_METHODS(f) => !reverted);
}

rule viewFunctionsDontUpdateState(env e, method f, calldataarg args) 
    filtered { f -> VIEW_METHODS(f) } {

    storage before = lastStorage;

    f(e, args);

    storage after = lastStorage;

    assert(before[currentContract] == after[currentContract]);
}