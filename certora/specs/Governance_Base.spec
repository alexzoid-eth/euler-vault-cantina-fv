import "base/base.spec";
import "methods/governor_methods.spec";

methods {
    // EVC functions summarize
    function _.requireVaultStatusCheck() external 
        => requireVaultStatusCheckCVL() expect void;
    function _.requireAccountAndVaultStatusCheck(address caller) external 
        => requireVaultAccountStatusCheckCVL(caller) expect void;
    function _.getCurrentOnBehalfOfAccount(address) external 
        => getCurrentOnBehalfOfAccountCVL() expect (address, bool) ALL;
}

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

// GOV-74 | Specific functions can modify state
use rule specificFunctionsModifyState;

// GOV-08 | Possibility of modifying state
use rule modifyStatePossibility;

// GOV-09 | Specific functions require a vault status check
rule specificFunctionsRequireVaultStatusCheck(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_METHODS(f) } {

    require(ghostRequireVaultStatusCheckCalled == false);

    f(e, args);
    
    assert(VAULT_STATUS_CHECK_METHODS(f) <=> ghostRequireVaultStatusCheckCalled);
}

// GOV-12 | State change functions are protected against reentrancy
use rule stateChangeFunctionsReentrancyProtected;

// GOV-13 | Functions are not able to receive native tokens
use rule notAbleReceiveNativeTokens;

// GOV-16 | Anyone can execute view functions
use rule anyoneCanExecuteViewFunctions;

// GOV-17 | View functions MUST NOT be protected against reentrancy
use rule viewFunctionsNotProtectedAgainstReentrancy;

// GOV-19 | View functions don't update state
use rule viewFunctionsDontUpdateState;