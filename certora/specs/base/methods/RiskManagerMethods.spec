import "./BaseMethods.spec";

methods {
    function accountLiquidity(address account, bool liquidation) external;
    function accountLiquidityFull(address account, bool liquidation) external;
    function disableController() external;
    function checkAccountStatus(address account, address[] collaterals) external;
    function checkVaultStatus() external returns (bytes4);
}

definition RISKMANAGER_HARNESS_METHODS(method f) returns bool = 
    BASE_HARNESS_METHODS(f);