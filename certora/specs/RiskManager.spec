import "./base/methods/RiskManagerMethods.spec";
import "./base/Base.spec";
import "./common/State.spec";
import "./common/Funcs.spec";

// RM-01 | Total shares and total borrows limitations
invariant totalSharesBorrowsLimits() 
    ghostTotalShares < MAX_SANE_AMOUNT() && ghostTotalBorrows < MAX_SANE_DEBT_AMOUNT()
    filtered { f -> !HARNESS_METHODS(f) }

// RM-02 | View functions don't update the state
use rule viewFunctionsDontUpdateState;

// RM-03 | Specific functions can modify state
use rule specificFunctionsModifyState;

// RM-04 | Possibility of modifying state
use rule modifyStatePossibility;

// RM-05 | Specific view functions are protected against reentrancy
use rule specificViewFunctionsProtectedAgainstReentrancy;

// RM-06 | Hook execution restriction
use rule hookExecutionRestriction;