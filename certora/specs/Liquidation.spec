import "./base/methods/LiquidationMethods.spec";
import "./base/Base.spec";
import "./common/State.spec";

// LIQ-01 | Liquidation operations are prohibited until the cool-down period has passed
rule liquidationCoolDownPeriodEnforced(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_METHODS(f) } {

    requireValidTimeStamp(e);

    f@withrevert(e, args);
    bool reverted = lastReverted;

    assert(ghostLastAccountStatusCheckTimestamp + ghostLiquidationCoolOffTime > to_mathint(e.block.timestamp) 
        => reverted
    );
}

// LIQ-02 | Check liquidation healthy
rule checkLiquidationHealthy() {
    env e;
    address liquidator;
    address violator; 
    address collateral;
    uint256 maxRepay;
    uint256 maxYield;

    require ghostOracleAddress != 0;

    uint256 liquidityCollateralValue;
    uint256 liquidityLiabilityValue;
    (liquidityCollateralValue, liquidityLiabilityValue) = 
        calculateLiquidityExt(e, violator);

    require liquidityCollateralValue > liquidityLiabilityValue;

    (maxRepay, maxYield) = checkLiquidation(e, liquidator, violator, collateral);

    assert maxRepay == 0;
    assert maxYield == 0;
}
