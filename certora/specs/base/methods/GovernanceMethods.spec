import "./BaseMethods.spec";

methods {

    // GovernanceHarness
    function isSenderGovernor() external returns (bool);

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
    ;

definition MODIFY_STATE_METHODS(method f) returns bool = 
    f.selector == sig:setGovernorAdmin(address).selector
    || f.selector == sig:setFeeReceiver(address).selector
    || f.selector == sig:setLTV(address,uint16,uint16,uint32).selector
    || f.selector == sig:clearLTV(address).selector
    || f.selector == sig:setMaxLiquidationDiscount(uint16).selector
    || f.selector == sig:setLiquidationCoolOffTime(uint16).selector
    || f.selector == sig:setInterestRateModel(address).selector
    || f.selector == sig:setHookConfig(address,uint32).selector
    || f.selector == sig:setConfigFlags(uint32).selector
    || f.selector == sig:setCaps(uint16,uint16).selector
    || f.selector == sig:setInterestFee(uint16).selector
    || f.selector == sig:convertFees().selector;

definition VIEW_METHODS(method f) returns bool = 
    f.selector == sig:governorAdmin().selector
    || f.selector == sig:feeReceiver().selector
    || f.selector == sig:interestFee().selector
    || f.selector == sig:interestRateModel().selector
    || f.selector == sig:protocolConfigAddress().selector
    || f.selector == sig:protocolFeeShare().selector
    || f.selector == sig:protocolFeeReceiver().selector
    || f.selector == sig:caps().selector
    || f.selector == sig:LTVBorrow(address).selector
    || f.selector == sig:LTVLiquidation(address).selector
    || f.selector == sig:LTVFull(address).selector
    || f.selector == sig:LTVList().selector
    || f.selector == sig:maxLiquidationDiscount().selector
    || f.selector == sig:liquidationCoolOffTime().selector
    || f.selector == sig:hookConfig().selector
    || f.selector == sig:configFlags().selector
    || f.selector == sig:EVC().selector
    || f.selector == sig:unitOfAccount().selector
    || f.selector == sig:oracle().selector
    || f.selector == sig:permit2Address().selector;

definition GOVERNOR_ONLY_METHODS(method f) returns bool = 
    f.selector == sig:setGovernorAdmin(address).selector
    || f.selector == sig:setFeeReceiver(address).selector
    || f.selector == sig:setLTV(address,uint16,uint16,uint32).selector
    || f.selector == sig:clearLTV(address).selector
    || f.selector == sig:setMaxLiquidationDiscount(uint16).selector
    || f.selector == sig:setLiquidationCoolOffTime(uint16).selector
    || f.selector == sig:setInterestRateModel(address).selector
    || f.selector == sig:setHookConfig(address,uint32).selector
    || f.selector == sig:setConfigFlags(uint32).selector
    || f.selector == sig:setCaps(uint16,uint16).selector
    || f.selector == sig:setInterestFee(uint16).selector;    

definition HARNESS_METHODS(method f) returns bool 
    = GOVERNANCE_HARNESS_METHODS(f);

function functionOperationCVL(method f) returns mathint {
    if(f.selector == sig:convertFees().selector) {
        return OP_CONVERT_FEES();
    } else {
        return 0;
    }
}

definition HOOK_METHODS(method f) returns bool = 
    f.selector == sig:convertFees().selector;