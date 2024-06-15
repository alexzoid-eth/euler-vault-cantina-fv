import "./BaseMethods.spec";

methods {

    // BorrowingHarness
    function initOperationExternal(uint32 operation, address accountToCheck) external returns (BorrowingHarness.VaultCache, address);
    function getTotalBalance() external returns (BorrowingHarness.Shares) envfree;
    function toAssetsExt(uint256 amount) external returns (uint256) envfree;
    function unpackBalanceExt(BorrowingHarness.PackedUserSlot data) external returns (BorrowingHarness.Shares) envfree;
    function getUserInterestAccExt(address account) external returns (uint256) envfree;
    function getVaultInterestAccExt() external returns (uint256);
    function getUnderlyingAssetExt() external returns (address);

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

definition BORROWING_HARNESS_METHODS(method f) returns bool = 
    BASE_HARNESS_METHODS(f)
    || f.selector == sig:initOperationExternal(uint32,address).selector
    || f.selector == sig:getTotalBalance().selector
    || f.selector == sig:toAssetsExt(uint256).selector
    || f.selector == sig:unpackBalanceExt(BorrowingHarness.PackedUserSlot).selector
    || f.selector == sig:getUserInterestAccExt(address).selector
    || f.selector == sig:getVaultInterestAccExt().selector
    || f.selector == sig:getUnderlyingAssetExt().selector
    ;