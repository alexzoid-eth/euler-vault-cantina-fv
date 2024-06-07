import "harness_methods.spec";

definition VAULT_HARNESS_METHODS(method f) returns bool = 
    ABSTRACT_BASE_HARNESS_METHODS(f)
    || f.selector == sig:userAssets(address).selector
    || f.selector == sig:storage_lastInterestAccumulatorUpdate().selector
    || f.selector == sig:storage_cash().selector
    || f.selector == sig:storage_supplyCap().selector
    || f.selector == sig:storage_borrowCap().selector
    || f.selector == sig:storage_hookedOps().selector
    || f.selector == sig:storage_snapshotInitialized().selector
    || f.selector == sig:storage_totalShares().selector
    || f.selector == sig:storage_totalBorrows().selector
    || f.selector == sig:storage_accumulatedFees().selector
    || f.selector == sig:storage_interestAccumulator().selector
    || f.selector == sig:storage_configFlags().selector
    || f.selector == sig:cache_cash().selector;
