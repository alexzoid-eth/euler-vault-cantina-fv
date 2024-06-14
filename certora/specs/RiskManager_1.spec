import "./base/RiskManager.spec";
import "./common/State.spec";

definition HARNESS_METHODS(method f) returns bool = RISKMANAGER_HARNESS_METHODS(f);

// RM1-01 | Total shares and total borrows limitations
invariant totalSharesBorrowsLimits() 
    ghostTotalShares < MAX_SANE_AMOUNT() && ghostTotalBorrows < MAX_SANE_DEBT_AMOUNT()
    filtered { f -> !HARNESS_METHODS(f) }
