import "./base/Base.spec";

// L2 | LTVFull() displays incorrect liquidation LTV
rule correctnessLTVFull(env e, address collateral) {

    uint16 borrowLTV;
    uint16 liquidationLTV;
    uint16 initialLiquidationLTV;
    uint48 targetTimestamp;
    uint32 rampDuration;
    borrowLTV, liquidationLTV, initialLiquidationLTV, targetTimestamp, rampDuration = LTVFull(e, collateral);

    assert(liquidationLTV == LTVLiquidation(e, collateral));
}