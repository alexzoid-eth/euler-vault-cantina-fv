import "./AbstractBase_Harness_methods.spec";

// List of harness functions selectors
definition GOVERNANCE_HARNESS_METHODS(method f) returns bool = 
    ABSTRACT_BASE_HARNESS_METHODS(f)
    || f.selector == sig:isSenderGovernor().selector
    ;