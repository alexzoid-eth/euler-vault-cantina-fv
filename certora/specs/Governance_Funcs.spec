import "./base/Governance.spec";
import "./common/Funcs.spec";

use builtin rule sanity;
use builtin rule hasDelegateCalls;
use builtin rule msgValueInLoopRule;

// GVF-01 | Specific functions can modify state
use rule specificFunctionsModifyState;

// GVF-02 | Possibility of modifying state
use rule modifyStatePossibility;

// GVF-03 | Specific functions require a vault status check
rule specificFunctionsRequireVaultStatusCheck(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_METHODS(f) } {

    require(ghostRequireVaultStatusCheckCalled == false);

    f(e, args);
    
    assert(VAULT_STATUS_CHECK_METHODS(f) <=> ghostRequireVaultStatusCheckCalled);
}

// GVF-04 | State change functions are protected against reentrancy
use rule stateChangeFunctionsReentrancyProtected;

// GVF-05 | Anyone can execute view functions
use rule anyoneCanExecuteViewFunctions;

// GVF-06 | View functions MUST NOT be protected against reentrancy
use rule viewFunctionsNotProtectedAgainstReentrancy;

// GVF-07 | View functions don't update state
use rule viewFunctionsDontUpdateState;