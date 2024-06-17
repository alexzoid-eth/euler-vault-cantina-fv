import "./BaseMethods.spec";

methods {
    // LiquidationHarness
    function calculateLiquidityExt(address account) external returns (uint256, uint256);
    function calculateLiquidationExt(LiquidationHarness.VaultCache vaultCache, address liquidator, address violator, address collateral, uint256 desiredRepay) external returns (LiquidationModule.LiquidationCache);
    function isRecognizedCollateralExt(address collateral) external returns (bool);
    function getCurrentOwedExt(LiquidationHarness.VaultCache vaultCache, address violator) external returns (LiquidationHarness.Assets) envfree;
    function getCollateralValueExt(LiquidationHarness.VaultCache vaultCache, address account, address collateral, bool liquidation) external returns (uint256);

    // Liquidation
    function checkLiquidation(address liquidator, address violator, address collateral) external returns (uint256, uint256);
    function liquidate(address violator, address collateral, uint256 repayAssets, uint256 minYieldBalance) external;
}

definition VIEW_REENTRANCY_PROTECTED_METHODS(method f) returns bool = 
    f.selector == sig:checkLiquidation(address,address,address).selector;

definition VIEW_METHODS(method f) returns bool = 
    VIEW_REENTRANCY_PROTECTED_METHODS(f);

definition MODIFY_STATE_METHODS(method f) returns bool = 
    f.selector == sig:liquidate(address,address,uint256,uint256).selector;

definition LIQUIDATION_HARNESS_METHODS(method f) returns bool = 
    BASE_HARNESS_METHODS(f)
    || f.selector == sig:calculateLiquidityExt(address).selector
    || f.selector == sig:calculateLiquidationExt(LiquidationHarness.VaultCache, address, address, address, uint256).selector
    || f.selector == sig:isRecognizedCollateralExt(address).selector
    || f.selector == sig:getCurrentOwedExt(LiquidationHarness.VaultCache, address).selector
    || f.selector == sig:getCollateralValueExt(LiquidationHarness.VaultCache, address, address, bool).selector
    ;

definition HARNESS_METHODS(method f) returns bool 
    = LIQUIDATION_HARNESS_METHODS(f);

function functionOperationCVL(method f) returns mathint {
    if(f.selector == sig:liquidate(address,address,uint256,uint256).selector) {
        return OP_LIQUIDATE();
    } else {
        return 0;
    }
}

definition HOOK_METHODS(method f) returns bool = 
    f.selector == sig:liquidate(address,address,uint256,uint256).selector;