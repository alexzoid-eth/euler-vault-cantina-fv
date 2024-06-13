import "./BaseMethods.spec";

methods {
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

definition BORROWING_HARNESS_METHODS(method f) returns bool = 
    BASE_HARNESS_METHODS(f);