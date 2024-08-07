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
    filtered { f -> !HARNESS_METHODS(f) && !f.isView } {

    bool locked = ghostReentrancyLocked;

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
    filtered { f -> VIEW_METHODS(f) } {

    reentrantViewSenderRequirementCVL(e1);
    reentrantViewSenderRequirementCVL(e2);

    require(e1.block.timestamp == e2.block.timestamp);

    require(e1.msg.value == 0 && e2.msg.value == 0);
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
    filtered { f -> f.isView && !HARNESS_METHODS(f) } {

    reentrantViewSenderRequirementCVL(e);

    require(ghostReentrancyLocked);

    f@withrevert(e, args);

    // Function could be executed when reentrancy in locked state
    satisfy(!lastReverted);
}

rule specificViewFunctionsProtectedAgainstReentrancy(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_METHODS(f) } {

    reentrantViewSenderRequirementCVL(e);

    require(ghostReentrancyLocked);

    f@withrevert(e, args);
    bool reverted = lastReverted;

    assert(VIEW_REENTRANCY_PROTECTED_METHODS(f) => reverted);
}

rule viewFunctionsDontUpdateState(env e, method f, calldataarg args) 
    filtered { f -> VIEW_METHODS(f) } {

    storage before = lastStorage;

    f(e, args);

    storage after = lastStorage;

    assert(before[currentContract] == after[currentContract]);
}

rule hookExecutionAllowance(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_METHODS(f) } {

    require(e.msg.sender == getEVC());

    require(ghostInvokeHookTargetCaller == 0);

    mathint opcode = functionOperationCVL(f);

    f(e, args);

    // Hook was executed
    assert(ghostInvokeHookTargetCaller != 0
        => (// Opcode is correct
            opcode != 0 
            // Hook execution is allowed
            && !isHookNotSet(require_uint32(opcode))
            // Caller is correct
            && ghostInvokeHookTargetCaller == ghostOnBehalfOfAccount
        )
    );
}

rule hookExecutionPossibility(env e, method f, calldataarg args) 
    filtered { f -> HOOK_METHODS(f) } {

    require(e.msg.sender == getEVC());

    require(ghostInvokeHookTargetCaller == 0);

    mathint opcode = functionOperationCVL(f);
    bool hookSet = !isHookNotSet(require_uint32(opcode));

    f(e, args);

    satisfy(hookSet
        => ghostInvokeHookTargetCaller == ghostOnBehalfOfAccount
        );
}

rule hookExecutionRestriction(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_METHODS(f) } {

    require(e.msg.sender == getEVC());

    require(ghostInvokeHookTargetCaller == 0);

    mathint opcode = functionOperationCVL(f);
    bool notSet = isHookNotSet(require_uint32(opcode));

    f(e, args);

    assert(opcode == 0 || notSet
        => ghostInvokeHookTargetCaller == 0
        );
}
