import "./BaseMethods.spec";

methods {
    // RiskManager
    function accountLiquidity(address account, bool liquidation) external;
    function accountLiquidityFull(address account, bool liquidation) external;
    function disableController() external;
    function checkAccountStatus(address account, address[] collaterals) external;
    function checkVaultStatus() external returns (bytes4);
}

definition VIEW_REENTRANCY_PROTECTED_METHODS(method f) returns bool = 
    f.selector == sig:accountLiquidity(address,bool).selector
    || f.selector == sig:accountLiquidityFull(address,bool).selector;

definition VIEW_METHODS(method f) returns bool = 
    VIEW_REENTRANCY_PROTECTED_METHODS(f);

definition MODIFY_STATE_METHODS(method f) returns bool = 
    f.selector == sig:checkVaultStatus().selector
    // || f.selector == sig:disableController().selector
    // || f.selector == sig:checkAccountStatus(address,address[]).selector
    ;

definition RISKMANAGER_HARNESS_METHODS(method f) returns bool 
    = BASE_HARNESS_METHODS(f);

definition HARNESS_METHODS(method f) returns bool 
    = RISKMANAGER_HARNESS_METHODS(f);

function functionOperationCVL(method f) returns mathint {
    return 0;
}