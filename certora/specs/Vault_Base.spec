import "base/vault_harness_methods.spec";
import "base/base.spec";

definition HARNESS_METHODS(method f) returns bool = VAULT_HARNESS_METHODS(f);

definition MODIFY_STATE_METHODS(method f) returns bool = 
    f.selector == sig:deposit(uint256,address).selector
    || f.selector == sig:mint(uint256,address).selector
    || f.selector == sig:withdraw(uint256,address,address).selector
    || f.selector == sig:redeem(uint256,address,address).selector
    || f.selector == sig:skim(uint256,address).selector;

definition VAULT_STATUS_CHECK_METHODS(method f) returns bool = 
    f.selector == sig:deposit(uint256,address).selector
    || f.selector == sig:mint(uint256,address).selector
    || f.selector == sig:skim(uint256,address).selector;

// VLT-01 | Specific functions require a vault status check
use rule specificFunctionsRequireVaultStatusCheck;