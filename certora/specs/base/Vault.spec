import "../methods/VaultMethods.spec";
import "./Base.spec";

definition HARNESS_METHODS(method f) returns bool = VAULT_HARNESS_METHODS(f);

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

definition VAULT_STATUS_CHECK_METHODS(method f) returns bool = 
    // Vault
    f.selector == sig:deposit(uint256,address).selector
    || f.selector == sig:mint(uint256,address).selector
    || f.selector == sig:skim(uint256,address).selector;

definition VAULT_ACCOUNT_STATUS_CHECK_METHODS(method f) returns bool = 
    // Vault
    f.selector == sig:withdraw(uint256,address,address).selector
    || f.selector == sig:redeem(uint256,address,address).selector
    // Token
    || f.selector == sig:transfer(address,uint256).selector
    || f.selector == sig:transferFromMax(address,address).selector
    || f.selector == sig:transferFrom(address,address,uint256).selector;

definition INPUT_METHODS(method f) returns bool = 
    f.selector == sig:deposit(uint256,address).selector
    || f.selector == sig:mint(uint256,address).selector;

definition OUTPUT_METHODS(method f) returns bool = 
    f.selector == sig:withdraw(uint256,address,address).selector
    || f.selector == sig:redeem(uint256,address,address).selector;
