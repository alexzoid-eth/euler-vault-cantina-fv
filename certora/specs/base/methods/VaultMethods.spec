import "./BaseMethods.spec";

methods {

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
    BASE_HARNESS_METHODS(f);