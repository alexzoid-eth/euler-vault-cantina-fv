import "./base/Liquidation.spec";
import "./common/State.spec";

definition HARNESS_METHODS(method f) returns bool = LIQUIDATION_HARNESS_METHODS(f);

// LQ-1 | Liquidation operations are prohibited until the cool-down period has passed
rule liquidationCoolDownPeriodEnforced(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_METHODS(f) } {

    requireValidTimeStamp(e);

    f@withrevert(e, args);
    bool reverted = lastReverted;

    assert(ghostLastAccountStatusCheckTimestamp + ghostLiquidationCoolOffTime > to_mathint(e.block.timestamp) 
        => reverted
    );
}