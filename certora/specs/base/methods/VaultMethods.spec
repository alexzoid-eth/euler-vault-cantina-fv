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

definition VAULT_HARNESS_METHODS(method f) returns bool = BASE_HARNESS_METHODS(f);

definition VIEW_REENTRANCY_PROTECTED_METHODS(method f) returns bool = 
    f.selector == sig:totalAssets().selector
    || f.selector == sig:convertToAssets(uint256).selector
    || f.selector == sig:convertToShares(uint256).selector
    || f.selector == sig:maxDeposit(address).selector
    || f.selector == sig:previewDeposit(uint256).selector
    || f.selector == sig:maxMint(address).selector
    || f.selector == sig:previewMint(uint256).selector
    || f.selector == sig:maxWithdraw(address).selector
    || f.selector == sig:previewWithdraw(uint256).selector
    || f.selector == sig:maxRedeem(address).selector
    || f.selector == sig:previewRedeem(uint256).selector
    || f.selector == sig:accumulatedFees().selector
    || f.selector == sig:accumulatedFeesAssets().selector
    || f.selector == sig:totalSupply().selector
    || f.selector == sig:balanceOf(address).selector
    || f.selector == sig:allowance(address,address).selector;

definition VIEW_METHODS(method f) returns bool = 
    VIEW_REENTRANCY_PROTECTED_METHODS(f)
    || f.selector == sig:asset().selector
    || f.selector == sig:creator().selector
    || f.selector == sig:name().selector
    || f.selector == sig:symbol().selector
    || f.selector == sig:decimals().selector;

definition MODIFY_STATE_METHODS(method f) returns bool = 
    // Vault
    f.selector == sig:deposit(uint256,address).selector
    || f.selector == sig:mint(uint256,address).selector
    || f.selector == sig:withdraw(uint256,address,address).selector
    || f.selector == sig:redeem(uint256,address,address).selector
    || f.selector == sig:skim(uint256,address).selector
    // Token
    || f.selector == sig:transfer(address,uint256).selector
    || f.selector == sig:transferFromMax(address,address).selector
    || f.selector == sig:transferFrom(address,address,uint256).selector
    || f.selector == sig:approve(address,uint256).selector;

definition INPUT_METHODS(method f) returns bool = 
    f.selector == sig:deposit(uint256,address).selector
    || f.selector == sig:mint(uint256,address).selector;

definition OUTPUT_METHODS(method f) returns bool = 
    f.selector == sig:withdraw(uint256,address,address).selector
    || f.selector == sig:redeem(uint256,address,address).selector;

definition HARNESS_METHODS(method f) returns bool = VAULT_HARNESS_METHODS(f);