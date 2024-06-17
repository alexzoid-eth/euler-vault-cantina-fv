methods {
    // AbstractBaseHarness
    function evcCompatibleAsset() external returns (bool) envfree;
    function isKnownNonOwnerAccountHarness(address account) external returns (bool) envfree;
    function LTVFullHarness(address collateral) external returns (uint16, uint16, uint16, uint48, uint32) envfree;
    function touchHarness() external;
    function getBorrowLTV(address collateral) external returns (uint16);
    function getLiquidationLTV(address collateral) external returns (uint16);
    function getAccountOwed(address account) external returns (uint256) envfree;
    function isBalanceAndBalanceEnabled(address account) external returns (bool) envfree;
    function isOperationDisabledExt(uint32 operation) external returns (bool);
    function isDepositDisabled() external returns (bool);
    function isMintDisabled() external returns (bool);
    function isWithdrawDisabled() external returns (bool);
    function isRedeemDisabled() external returns (bool);
    function isSkimDisabled() external returns (bool);
    function isHookNotSet(uint32 flag) external returns (bool) envfree;
    function collateralExists(address collateral) external returns (bool) envfree;
    function ltvListLength() external returns (uint256) envfree;
    function storage_supplyCap() external returns (uint256) envfree;
    function storage_borrowCap() external returns (uint256) envfree;
    function getEVC() external returns (address) envfree;
}

definition BASE_HARNESS_METHODS(method f) returns bool = 
    f.selector == sig:evcCompatibleAsset().selector
    || f.selector == sig:isKnownNonOwnerAccountHarness(address).selector
    || f.selector == sig:LTVFullHarness(address).selector
    || f.selector == sig:getAccountOwed(address).selector
    || f.selector == sig:touchHarness().selector
    || f.selector == sig:getBorrowLTV(address).selector
    || f.selector == sig:getLiquidationLTV(address).selector
    || f.selector == sig:isBalanceAndBalanceEnabled(address).selector
    || f.selector == sig:isOperationDisabledExt(uint32).selector
    || f.selector == sig:isDepositDisabled().selector
    || f.selector == sig:isMintDisabled().selector
    || f.selector == sig:isWithdrawDisabled().selector
    || f.selector == sig:isRedeemDisabled().selector
    || f.selector == sig:isSkimDisabled().selector
    || f.selector == sig:isHookNotSet(uint32).selector
    || f.selector == sig:collateralExists(address).selector
    || f.selector == sig:ltvListLength().selector
    || f.selector == sig:storage_supplyCap().selector
    || f.selector == sig:storage_borrowCap().selector
    || f.selector == sig:getEVC().selector
    ;

definition HARNESS_VIEW_METHODS(method f) returns bool 
    = HARNESS_METHODS(f) || f.isView;