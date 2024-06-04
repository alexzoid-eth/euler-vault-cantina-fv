methods {
    function governorAdmin() external returns (address) envfree;
    function setGovernorAdmin(address newGovernorAdmin) external;  
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