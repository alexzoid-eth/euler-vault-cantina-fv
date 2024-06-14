methods {
    
    // AbstractBaseHarness
    function LTVFullHarness(address collateral) external returns (uint16, uint16, uint16, uint48, uint32) envfree;
    function touchHarness() external;
    function getBorrowLTV(address collateral) external returns (uint16);
    function getLiquidationLTV(address collateral) external returns (uint16);
    function debtOfExactHarness(address account) external returns (uint256);
    function borrowsToAssetsUp(uint256 amount) external returns (uint256) envfree;
    function vaultCacheOracleConfigured() external returns (bool);
    function isAccountStatusCheckDeferredExt(address account) external returns (bool);
    function getBalance(address account) external returns (uint256) envfree;
    function isBalanceAndBalanceEnabled(address account) external returns (bool) envfree;
    function vaultIsOnlyController(address account) external returns (bool);
    function vaultIsController(address account) external returns (bool);
    function getCollateralsExt(address account) external returns (address[] memory);
    function isCollateralEnabledExt(address account, address market) external returns (bool);
    function isOperationDisabledExt(uint32 operation) external returns (bool);
    function isDepositDisabled() external returns (bool);
    function isMintDisabled() external returns (bool);
    function isWithdrawDisabled() external returns (bool);
    function isRedeemDisabled() external returns (bool);
    function isSkimDisabled() external returns (bool);
    function reentrancyLocked() external returns (bool) envfree;
    function hookTarget() external returns (address) envfree;
    function totalShares() external returns (uint256);
    function isHookNotSetConvertFees() external returns (bool) envfree;
    function collateralExists(address collateral) external returns (bool) envfree;
    function ltvListLength() external returns (uint256) envfree;
    function storage_lastInterestAccumulatorUpdate() external returns (uint48) envfree;
    function storage_cash() external returns (BaseHarness.Assets) envfree;
    function storage_supplyCap() external returns (uint256) envfree;
    function storage_borrowCap() external returns (uint256) envfree;
    function storage_hookedOps() external returns (BaseHarness.Flags) envfree;
    function storage_snapshotInitialized() external returns (bool) envfree;
    function storage_totalShares() external returns (BaseHarness.Shares) envfree;
    function storage_totalBorrows() external returns (BaseHarness.Owed) envfree;
    function storage_accumulatedFees() external returns (BaseHarness.Shares) envfree;
    function storage_interestAccumulator() external returns (uint256) envfree;
    function storage_configFlags() external returns (BaseHarness.Flags) envfree;
    function cache_cash() external returns (BaseHarness.Assets);
}

definition BASE_HARNESS_METHODS(method f) returns bool = 
    f.selector == sig:initialize(address).selector
    || f.selector == sig:LTVFullHarness(address).selector
    || f.selector == sig:debtOfExactHarness(address).selector
    || f.selector == sig:touchHarness().selector
    || f.selector == sig:borrowsToAssetsUp(uint256).selector
    || f.selector == sig:vaultCacheOracleConfigured().selector
    || f.selector == sig:isAccountStatusCheckDeferredExt(address).selector
    || f.selector == sig:getBalance(address).selector
    || f.selector == sig:isBalanceAndBalanceEnabled(address).selector
    || f.selector == sig:vaultIsOnlyController(address).selector
    || f.selector == sig:vaultIsController(address).selector
    || f.selector == sig:getCollateralsExt(address).selector
    || f.selector == sig:isCollateralEnabledExt(address, address).selector
    || f.selector == sig:isOperationDisabledExt(uint32).selector
    || f.selector == sig:isDepositDisabled().selector
    || f.selector == sig:isMintDisabled().selector
    || f.selector == sig:isWithdrawDisabled().selector
    || f.selector == sig:isRedeemDisabled().selector
    || f.selector == sig:isSkimDisabled().selector
    || f.selector == sig:reentrancyLocked().selector
    || f.selector == sig:hookTarget().selector
    || f.selector == sig:totalShares().selector
    || f.selector == sig:isHookNotSetConvertFees().selector
    || f.selector == sig:collateralExists(address).selector
    || f.selector == sig:ltvListLength().selector
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
    || f.selector == sig:cache_cash().selector
    ;
