import "./base/methods/BorrowingMethods.spec";
import "./base/Base.spec";
import "./common/State.spec";
import "./common/Funcs.spec";

use builtin rule sanity;
use builtin rule msgValueInLoopRule;

// BRW-01 | View functions don't update the state
use rule viewFunctionsDontUpdateState;

// BRW-02 | State change functions are protected against reentrancy
use rule stateChangeFunctionsReentrancyProtected;

// BRW-03 | Specific functions can modify state
use rule specificFunctionsModifyState;

// BRW-04 | Possibility of modifying state
use rule modifyStatePossibility;

// BRW-05 | Specific view functions are protected against reentrancy
use rule specificViewFunctionsProtectedAgainstReentrancy;

// BRW-06 | Hook execution allowance
use rule hookExecutionAllowance;

// BRW-07 | Hook execution possibility
use rule hookExecutionPossibility;

// BRW-08 | Hook execution restriction
use rule hookExecutionRestriction;