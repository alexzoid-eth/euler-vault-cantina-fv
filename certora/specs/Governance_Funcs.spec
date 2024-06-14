import "./base/Governance.spec";
import "./common/Funcs.spec";

use builtin rule sanity;
use builtin rule hasDelegateCalls;
use builtin rule msgValueInLoopRule;

// GOV-74 | Specific functions can modify state
use rule specificFunctionsModifyState;

// GOV-08 | Possibility of modifying state
use rule modifyStatePossibility;

// GOV-09 | Specific functions require a vault status check
rule specificFunctionsRequireVaultStatusCheck(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_METHODS(f) } {

    require(ghostRequireVaultStatusCheckCalled == false);

    f(e, args);
    
    assert(VAULT_STATUS_CHECK_METHODS(f) <=> ghostRequireVaultStatusCheckCalled);
}

// GOV-12 | State change functions are protected against reentrancy
use rule stateChangeFunctionsReentrancyProtected;

// GOV-16 | Anyone can execute view functions
use rule anyoneCanExecuteViewFunctions;

// GOV-17 | View functions MUST NOT be protected against reentrancy
use rule viewFunctionsNotProtectedAgainstReentrancy;

// GOV-19 | View functions don't update state
use rule viewFunctionsDontUpdateState;