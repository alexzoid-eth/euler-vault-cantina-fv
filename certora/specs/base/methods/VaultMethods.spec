import "./BaseMethods.spec";

methods {

    // Token
    function name() external returns (string memory) envfree;
    function symbol() external returns (string memory) envfree;
    function decimals() external returns (uint8) envfree;
    function totalSupply() external returns (uint256);
    function balanceOf(address account) external returns (uint256);
    function allowance(address holder, address spender) external returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
    function transferFromMax(address from, address to) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function approve(address spender, uint256 amount) external returns (bool);

    // Vault
    function asset() external returns (address) envfree;
    function totalAssets() external returns (uint256);
    function convertToAssets(uint256 shares) external returns (uint256);
    function convertToShares(uint256 assets) external returns (uint256);
    function maxDeposit(address account) external returns (uint256);
    function previewDeposit(uint256 assets) external returns (uint256);
    function maxMint(address account) external returns (uint256);
    function previewMint(uint256 shares) external returns (uint256);
    function maxWithdraw(address owner) external returns (uint256);
    function previewWithdraw(uint256 assets) external returns (uint256);
    function maxRedeem(address owner) external returns (uint256);
    function previewRedeem(uint256 shares) external returns (uint256);
    function accumulatedFees() external returns (uint256);
    function accumulatedFeesAssets() external returns (uint256);
    function creator() external returns (address) envfree;
    function deposit(uint256 amount, address receiver) external;
    function mint(uint256 amount, address receiver) external;
    function withdraw(uint256 amount, address receiver, address owner) external;
    function redeem(uint256 amount, address receiver, address owner) external;
    function skim(uint256 amount, address receiver) external;
}

definition VAULT_HARNESS_METHODS(method f) returns bool = 
    BASE_HARNESS_METHODS(f);