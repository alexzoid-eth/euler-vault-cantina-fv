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

// L1-EX | Ensure that protocol fee receiver gets an amount of shares equal to what `protocolFeeShare()` getter returns
rule protocolFeeShareLimitedEx(env e, method f, calldataarg args) {

    // Retrieve the addresses for the governor and protocol fee receivers
    address governor = feeReceiver();
    address protocol = ghostProtocolFeeReceiver[currentContract];

    // Safe assumption: ensure that the governor fee receiver is set and is not the same as the protocol fee receiver
    require(governor != 0);
    require(governor != protocol);

    // Get the expected protocol fee shares based on the `protocolFeeShare()` getter
    mathint getterFeeShare = to_mathint(protocolFeeShare(e));
    mathint governorExpectShares = (ghostAccumulatedFees * (CONFIG_SCALE() - getterFeeShare)) / CONFIG_SCALE();
    mathint protocolExpectShares = ghostAccumulatedFees - governorExpectShares;

    // Capture the protocol fee receiver's balance before the function call
    mathint protocolBalanceBefore = ghostUsersDataBalance[protocol];

    // Execute any external function
    f(e, args);

    // Capture the protocol fee receiver's balance after the function call
    mathint protocolBalanceAfter = ghostUsersDataBalance[protocol];

    // Ensure that any change in the protocol fee receiver's balance is as expected
    // The increase in protocol fee receiver shares MUST equal the expectations based on the `protocolFeeShare()` getter
    assert(protocolBalanceAfter != protocolBalanceBefore 
        => protocolBalanceAfter - protocolBalanceBefore == protocolExpectShares
    );
}