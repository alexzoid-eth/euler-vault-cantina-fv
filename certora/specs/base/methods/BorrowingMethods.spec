import "./BaseMethods.spec";

methods {

    // BorrowingHarness

    // Borrowing
    function totalBorrows() external returns (uint256);
    function totalBorrowsExact() external returns (uint256);
    function cash() external returns (uint256);
    function debtOf(address account) external returns (uint256);
    function debtOfExact(address account) external returns (uint256);
    function interestRate() external returns (uint256);
    function interestAccumulator() external returns (uint256);
    function dToken() external returns (address) envfree;
    function borrow(uint256 amount, address receiver) external returns (uint256);
    function repay(uint256 amount, address receiver) external returns (uint256);
    function repayWithShares(uint256 amount, address receiver) external returns (uint256, uint256);
    function pullDebt(uint256 amount, address from) external returns (uint256);
    function flashLoan(uint256 amount, bytes calldata data) external;
    function touch() external;
}

definition VIEW_REENTRANCY_PROTECTED_METHODS(method f) returns bool = 
    f.selector == sig:totalBorrows().selector
    || f.selector == sig:totalBorrowsExact().selector
    || f.selector == sig:cash().selector
    || f.selector == sig:debtOf(address).selector
    || f.selector == sig:debtOfExact(address).selector
    || f.selector == sig:interestRate().selector
    || f.selector == sig:interestAccumulator().selector;

definition VIEW_METHODS(method f) returns bool = 
    VIEW_REENTRANCY_PROTECTED_METHODS(f)
    || f.selector == sig:dToken().selector;

definition MODIFY_STATE_METHODS(method f) returns bool = 
    f.selector == sig:borrow(uint256,address).selector
    || f.selector == sig:repay(uint256,address).selector
    || f.selector == sig:repayWithShares(uint256,address).selector
    || f.selector == sig:pullDebt(uint256,address).selector
    // || f.selector == sig:flashLoan(uint256,bytes).selector
    || f.selector == sig:touch().selector;

definition BORROWING_HARNESS_METHODS(method f) returns bool = 
    BASE_HARNESS_METHODS(f)
    ;

definition HARNESS_METHODS(method f) returns bool 
    = BORROWING_HARNESS_METHODS(f);

function functionOperationCVL(method f) returns mathint {
    if(f.selector == sig:borrow(uint256,address).selector) {
        return OP_BORROW();
    } else if(f.selector == sig:repay(uint256,address).selector) {
        return OP_REPAY();
    } else if(f.selector == sig:repayWithShares(uint256,address).selector) {
        return OP_REPAY_WITH_SHARES();
    } else if(f.selector == sig:pullDebt(uint256,address).selector) {
        return OP_PULL_DEBT();
    } else if(f.selector == sig:flashLoan(uint256,bytes).selector) {
        return OP_FLASHLOAN();
    } else if(f.selector == sig:touch().selector) {
        return OP_TOUCH();
    } else {
        return 0;
    }
}

definition HOOK_METHODS(method f) returns bool = 
    f.selector == sig:borrow(uint256,address).selector
    || f.selector == sig:repay(uint256,address).selector
    || f.selector == sig:repayWithShares(uint256,address).selector
    || f.selector == sig:pullDebt(uint256,address).selector
    || f.selector == sig:flashLoan(uint256,bytes).selector
    || f.selector == sig:touch().selector;