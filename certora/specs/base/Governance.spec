import "./methods/GovernanceMethods.spec";
import "./Base.spec";

definition HARNESS_METHODS(method f) returns bool = 
    GOVERNANCE_HARNESS_METHODS(f);

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

definition VAULT_STATUS_CHECK_METHODS(method f) returns bool = 
    f.selector == sig:convertFees().selector;

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