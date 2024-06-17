import "./base/methods/RiskManagerMethods.spec";
import "./base/Base.spec";
import "./common/State.spec";

// RM-01 | Total shares and total borrows limitations
invariant totalSharesBorrowsLimits() 
    ghostTotalShares < MAX_SANE_AMOUNT() && ghostTotalBorrows < MAX_SANE_DEBT_AMOUNT()
    filtered { f -> !HARNESS_METHODS(f) }
