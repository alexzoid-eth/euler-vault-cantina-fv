import "./base/Governance.spec";

using ProtocolConfig as _ProtocolConfig;

methods {
    function _ProtocolConfig.isValidInterestFee(address vault, uint16 interestFee) external;
    function _ProtocolConfig.protocolFeeConfig(address vault) external;
}

// protocolFeeShare() displays icorrect value as it doesn't consider 50% limit
rule protocolFeeShareLimit(env e) {
    assert(to_mathint(LTVLiquidation(e)) <= MAX_PROTOCOL_FEE_SHARE());
}