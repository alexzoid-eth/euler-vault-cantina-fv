import "./base/Vault.spec";
import "./common/Funcs.spec";

use builtin rule sanity;
use builtin rule hasDelegateCalls;
use builtin rule msgValueInLoopRule;

// VLT-01 | Specific functions require a vault status check
rule specificFunctionsRequireVaultStatusCheck(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_METHODS(f) } {

    require(ghostRequireVaultStatusCheckCalled == false);

    uint256 amount;
    address receiver;
    address owner;
    require(owner != 0); // Prevent CHECKACCOUNT_NONE usage, with zero owner function will always revert

    if(f.selector == sig:withdraw(uint256, address, address).selector) {
        withdraw(e, amount, receiver, owner);
    } else if(f.selector == sig:redeem(uint256, address, address).selector) {
        redeem(e, amount, receiver, owner);
    } else {
        f(e, args);
    }
    
    assert(VAULT_STATUS_CHECK_METHODS(f) <=> ghostRequireVaultStatusCheckCalled);
}

// VLT-02 | Specific functions require a vault and account status check
rule specificFunctionsRequireVaultAccountStatusCheck(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_METHODS(f) } {

    require(ghostRequireVaultAccountStatusCheckCalled == false);

    uint256 amount;
    address receiver;
    address owner;
    require(owner != 0); // Prevent CHECKACCOUNT_NONE usage, with zero owner function will always revert

    if(f.selector == sig:withdraw(uint256, address, address).selector) {
        withdraw(e, amount, receiver, owner);
    } else if(f.selector == sig:redeem(uint256, address, address).selector) {
        redeem(e, amount, receiver, owner);
    } else {
        f(e, args);
    }

    assert(VAULT_ACCOUNT_STATUS_CHECK_METHODS(f) <=> ghostRequireVaultAccountStatusCheckCalled);
}

// VLT-05 | State change functions are protected against reentrancy
use rule stateChangeFunctionsReentrancyProtected;

// VLT-07 | Anyone can execute view functions
use rule anyoneCanExecuteViewFunctions;

// VLT-08 | Specific view functions are protected against reentrancy, while others are not
use rule specificViewFunctionsProtectedAgainstReentrancy;

// VLT-10 | View functions don't update the state
use rule viewFunctionsDontUpdateState;
