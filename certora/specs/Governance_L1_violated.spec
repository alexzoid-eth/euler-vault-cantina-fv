import "./base/methods/GovernanceMethods.spec";
import "./base/Base.spec";

using ProtocolConfig as _ProtocolConfig;

methods {
    function _ProtocolConfig.isValidInterestFee(address vault, uint16 interestFee) external;
    function _ProtocolConfig.protocolFeeConfig(address vault) external;
}

// L1 | `protocolFeeShare()` displays icorrect value as it doesn't consider 50% limitation
rule protocolFeeShareLimited(env e) {
    assert(to_mathint(protocolFeeShare(e)) <= MAX_PROTOCOL_FEE_SHARE());
}