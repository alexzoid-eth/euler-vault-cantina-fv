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

// L1-EX | Ensure that protocol fee receiver never gets more fees than `protocolFeeShare()` getter returns 
rule protocolFeeShareLimitedEx(env e, method f, calldataarg args) {

    address governor = feeReceiver();
    address protocol = ghostProtocolFeeReceiver[currentContract];

    // Safe assumption: governor fee receiver is set and not equal to protocol fee receiver
    require(governor != 0);
    require(governor != protocol);

    // Protocol shares expectations based on `protocolFeeShare()` getter
    mathint getterFeeShare = to_mathint(protocolFeeShare(e));
    mathint governorExpectShares = (ghostAccumulatedFees * (CONFIG_SCALE() - getterFeeShare)) / CONFIG_SCALE();
    mathint protocolExpectShares = ghostAccumulatedFees - governorExpectShares;

    // Protocol shares before
    mathint protocolBalanceBefore = ghostUsersDataBalance[protocol];

    f(e, args);

    // Protocol shares increase after
    mathint protocolGotShares = ghostUsersDataBalance[protocol] - protocolBalanceBefore;

    // Protocol MUST NOT receive more than expected with `protocolFeeShare()` (1 wei rounding tolerance)
    assert(protocolExpectShares >= protocolGotShares);
}