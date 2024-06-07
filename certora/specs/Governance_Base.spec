import "base/governor_harness_methods.spec";
import "base/base.spec";

definition HARNESS_METHODS(method f) returns bool = GOVERNANCE_HARNESS_METHODS(f);

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

definition VAULT_STATUS_CHECK_METHODS(method f) returns bool = 
    f.selector == sig:convertFees().selector;

// GOV-74 | Specific functions can modify state
use rule specificFunctionsModifyState;

// GOV-08 | Possibility of modifying state
use rule modifyStatePossibility;

// GOV-09 | Specific functions require a vault status check
use rule specificFunctionsRequireVaultStatusCheck;

// GOV-12 | State change functions are protected against reentrancy
use rule stateChangeFunctionsReentrancyProtected;

// GOV-13 | Functions are not able to receive native tokens
use rule notAbleReceiveNativeTokens;