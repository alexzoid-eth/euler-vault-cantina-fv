import "harness_methods.spec";

definition GOVERNANCE_HARNESS_METHODS(method f) returns bool = 
    ABSTRACT_BASE_HARNESS_METHODS(f)
    || f.selector == sig:isSenderGovernor().selector
    || f.selector == sig:accumulatedFees().selector
    ;
