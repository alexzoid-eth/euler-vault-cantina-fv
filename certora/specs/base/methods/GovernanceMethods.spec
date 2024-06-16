import "./BaseMethods.spec";

methods {

    // GovernanceHarness
    function isSenderGovernor() external returns (bool);
    function accumulatedFees() external returns (uint256);
    function getLTVConfig(address) external returns (BaseHarness.LTVConfig memory) envfree;
    function getBalanceAndForwarderExt(address) external returns (BaseHarness.Shares, bool) envfree;

    // Governance
    function governorAdmin() external returns (address) envfree;
    function feeReceiver() external returns (address) envfree;
    function interestFee() external returns (uint16) envfree;
    function interestRateModel() external returns (address) envfree;
    function protocolConfigAddress() external returns (address) envfree;
    function protocolFeeShare() external returns (uint256);
    function protocolFeeReceiver() external returns (address);
    function caps() external returns (uint16, uint16) envfree;
    function LTVBorrow(address) external returns (uint16);
    function LTVLiquidation(address) external returns (uint16);
    function LTVFull(address) external returns (uint16, uint16, uint16, uint48, uint32); // Not set as envfree to support issue fix
    function LTVList() external returns (address[] memory) envfree;
    function maxLiquidationDiscount() external returns (uint16) envfree;
    function liquidationCoolOffTime() external returns (uint16) envfree;
    function hookConfig() external returns (address, uint32) envfree;
    function configFlags() external returns (uint32) envfree;
    function EVC() external returns (address) envfree;
    function unitOfAccount() external returns (address) envfree;
    function oracle() external returns (address) envfree;
    function permit2Address() external returns (address) envfree;
    function convertFees() external;
    function setGovernorAdmin(address) external;
    function setFeeReceiver(address) external;
    function setLTV(address, uint16, uint16, uint32) external;
    function clearLTV(address) external;
    function setMaxLiquidationDiscount(uint16) external;
    function setLiquidationCoolOffTime(uint16) external;
    function setInterestRateModel(address) external;
    function setHookConfig(address, uint32) external;
    function setConfigFlags(uint32) external;
    function setCaps(uint16, uint16) external;
    function setInterestFee(uint16) external;
}

definition GOVERNANCE_HARNESS_METHODS(method f) returns bool = 
    BASE_HARNESS_METHODS(f)
    || f.selector == sig:isSenderGovernor().selector
    || f.selector == sig:accumulatedFees().selector
    || f.selector == sig:getLTVConfig(address).selector
    || f.selector == sig:getBalanceAndForwarderExt(address).selector
    ;
