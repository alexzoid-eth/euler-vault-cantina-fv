import "./base/methods/LiquidationMethods.spec";
import "./base/Base.spec";
import "./common/State.spec";
import "./common/Funcs.spec";

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

// LIQ-03 | View functions don't update the state
use rule viewFunctionsDontUpdateState;

// LIQ-04 | State change functions are protected against reentrancy
use rule stateChangeFunctionsReentrancyProtected;

// LIQ-05 | Specific functions can modify state
use rule specificFunctionsModifyState;

// LIQ-06 | Possibility of modifying state
use rule modifyStatePossibility;

// LIQ-07 | Specific view functions are protected against reentrancy
use rule specificViewFunctionsProtectedAgainstReentrancy;

// LIQ-08 | Possibility of liquidation
rule liquidationPossibility(
    env e, address liquidator, address violator, address collateral, uint256 repayAssets, uint256 minYieldBalance
    ) {

    uint256 maxRepayBefore;
    uint256 maxYieldBefore;
    (maxRepayBefore, maxYieldBefore) = checkLiquidation(e, liquidator, violator, collateral);

    liquidate(e, violator, collateral, repayAssets, minYieldBalance);

    uint256 maxRepayAfter;
    uint256 maxYieldAfter;
    (maxRepayAfter, maxYieldAfter) = checkLiquidation(e, liquidator, violator, collateral);

    satisfy(maxRepayBefore != 0 && maxYieldBefore != 0
        => maxRepayAfter == 0 && maxYieldAfter == 0
    );
}

// LIQ-09 | Hook execution allowance
use rule hookExecutionAllowance;

// LIQ-10 | Hook execution possibility
use rule hookExecutionPossibility;

// LIQ-11 | Hook execution restriction
use rule hookExecutionRestriction;