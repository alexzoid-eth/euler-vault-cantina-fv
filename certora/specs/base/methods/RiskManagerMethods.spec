import "./BaseMethods.spec";

methods {
    // RiskManager
    function accountLiquidity(address account, bool liquidation) external;
    function accountLiquidityFull(address account, bool liquidation) external;
    function disableController() external;
    function checkAccountStatus(address account, address[] collaterals) external;
    function checkVaultStatus() external returns (bytes4);
}

definition RISKMANAGER_HARNESS_METHODS(method f) returns bool = BASE_HARNESS_METHODS(f);

definition HARNESS_METHODS(method f) returns bool = RISKMANAGER_HARNESS_METHODS(f);