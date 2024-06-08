import "./base/Governance.spec";

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