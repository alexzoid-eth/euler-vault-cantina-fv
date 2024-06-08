methods {

    // VaultHarness
    function userAssets(address) external returns (uint256);
    function storage_lastInterestAccumulatorUpdate() external returns (uint48) envfree;
    function storage_cash() external returns (VaultHarness.Assets) envfree;
    function storage_supplyCap() external returns (uint256) envfree;
    function storage_borrowCap() external returns (uint256) envfree;
    function storage_hookedOps() external returns (VaultHarness.Flags) envfree;
    function storage_snapshotInitialized() external returns (bool) envfree;
    function storage_totalShares() external returns (VaultHarness.Shares) envfree;
    function storage_totalBorrows() external returns (VaultHarness.Owed) envfree;
    function storage_accumulatedFees() external returns (VaultHarness.Shares) envfree;
    function storage_interestAccumulator() external returns (uint256) envfree;
    function storage_configFlags() external returns (VaultHarness.Flags) envfree;
    function cache_cash() external returns (VaultHarness.Assets);

    // Token
    function name() external returns (string) envfree;
    function symbol() external returns (string) envfree;
    function decimals() external returns (uint8) envfree;
    function totalSupply() external returns (uint256);
    function balanceOf(address) external returns (uint256);
    function allowance(address, address) external returns (uint256);
    function transfer(address, uint256) external returns (bool);
    function transferFromMax(address, address) external returns (bool);
    function transferFrom(address, address, uint256) external returns (bool);
    function approve(address, uint256) external returns (bool);

    // Vault
    function asset() external returns (address) envfree;
    function totalAssets() external returns (uint256);
    function convertToAssets(uint256) external returns (uint256);
    function convertToShares(uint256) external returns (uint256);
    function maxDeposit(address) external returns (uint256);
    function previewDeposit(uint256) external returns (uint256);
    function maxMint(address) external returns (uint256);
    function previewMint(uint256) external returns (uint256);
    function maxWithdraw(address) external returns (uint256);
    function previewWithdraw(uint256) external returns (uint256);
    function maxRedeem(address) external returns (uint256);
    function previewRedeem(uint256) external returns (uint256);
    function accumulatedFees() external returns (uint256);
    function accumulatedFeesAssets() external returns (uint256);
    function creator() external returns (address) envfree;
    function deposit(uint256, address) external;
    function mint(uint256, address) external;
    function withdraw(uint256, address, address) external;
    function redeem(uint256, address, address) external;
    function skim(uint256, address) external;
}

definition VAULT_HARNESS_METHODS(method f) returns bool = 
    BASE_HARNESS_METHODS(f)
    || f.selector == sig:userAssets(address).selector
    || f.selector == sig:storage_lastInterestAccumulatorUpdate().selector
    || f.selector == sig:storage_cash().selector
    || f.selector == sig:storage_supplyCap().selector
    || f.selector == sig:storage_borrowCap().selector
    || f.selector == sig:storage_hookedOps().selector
    || f.selector == sig:storage_snapshotInitialized().selector
    || f.selector == sig:storage_totalShares().selector
    || f.selector == sig:storage_totalBorrows().selector
    || f.selector == sig:storage_accumulatedFees().selector
    || f.selector == sig:storage_interestAccumulator().selector
    || f.selector == sig:storage_configFlags().selector
    || f.selector == sig:cache_cash().selector;
