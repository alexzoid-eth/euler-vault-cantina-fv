import "./methods/BaseMethods.spec";
import "./RPow.spec";
import "./StorageHooks.spec";
import "./StorageHooksAsset.spec";
import "./LoadVault.spec";

methods {

    //
    // Internal
    //
    
    // Resolve asset to DummyERC20A
    function ProxyUtils.metadata() internal returns (address, address, address) 
        => metadataCVL();

    function _.mulDiv(uint144 a, uint256 b, uint256 c) internal => CVLMulDiv(a, b, c) expect uint144;

    function _.trySafeTransferFrom(address token, address from, address to, uint256 value) internal with (env e) 
        => trySafeTransferFromCVL(e, from, to, value) expect (bool, bytes memory);
    function _.safeTransferFrom(address token, address from, address to, uint256 value, address permit2) internal with (env e)
        => trySafeTransferFromCVL(e, from, to, value) expect (bool, bytes memory);

    function RPow.rpow(uint256 x, uint256 y, uint256 base) internal returns (uint256, bool) 
        => CVLPow(x, y, base);

    function _.logVaultStatus(BaseHarness.VaultCache memory a, uint256 interestRate) internal 
        => logVaultStatusCVL(interestRate) expect void;

    function Cache.loadVault() internal returns (BaseHarness.VaultCache memory) with (env e) 
        => loadVaultAssumeNoUpdateCVL(e);

    function _.hasAnyControllerEnabled(address caller) internal 
        => hasAnyControllerEnabledCVL(caller) expect bool;

    function _.invokeHookTarget(address caller) internal => NONDET;
    function _.calculateDTokenAddress() internal => NONDET;

    //
    // HookTarget
    // 

    function _.isHookTarget() external => NONDET;

    //
    // DToken
    // 

    function _.emitTransfer(address from, address to, uint256 value) external => NONDET;

    //
    // BalanceForwarder
    //

    function _.balanceTrackerHook(address account, uint256 newAccountBalance, bool forfeitRecentReward) external 
        => balanceTrackerHookCVL(account, newAccountBalance, forfeitRecentReward) expect void;

    //
    // PriceOracle
    //

    function _.getQuote(uint256 amount, address base, address quote) external 
        => CVLGetQuote(amount, base, quote) expect (uint256);

    function _.getQuotes(uint256 amount, address base, address quote) external 
        => CVLGetQuotes(amount, base, quote) expect (uint256, uint256);

    //
    // ProtocolConfig
    //

    function _.isValidInterestFee(address vault, uint16 interestFee) external => NONDET;

    function _.protocolFeeConfig(address vault) external 
        => protocolFeeConfigCVL(vault) expect (address, uint16) ALL;

    //
    // IRM
    //

    function _.computeInterestRate(address vault, uint256 cash, uint256 borrows) external 
        => computeInterestRateCVL(vault, cash, borrows) expect uint256 ALL;
    function _.computeInterestRateView(address vault, uint256 cash, uint256 borrows) external 
        => computeInterestRateCVL(vault, cash, borrows) expect uint256 ALL;

    //
    // FlashLoan
    //

    function _.onFlashLoan(bytes) external => NONDET;

    //
    // Asset
    //
    
	function _.name() external => DISPATCHER(true);
    function _.symbol() external => DISPATCHER(true);
    function _.decimals() external => DISPATCHER(true);
    function _.totalSupply() external => DISPATCHER(true);
    function _.balanceOf(address account) external => DISPATCHER(true);
    function _.allowance(address owner, address spender) external => DISPATCHER(true);
    function _.approve(address spender, uint256 amount) external => DISPATCHER(true);
    function _.transfer(address recipient, uint256 amount) external => DISPATCHER(true);
    function _.transferFrom(address sender, address recipient, uint256 amount) external => DISPATCHER(true);

    //
    // EVC
    //

    function _.requireVaultStatusCheck() external 
        => requireVaultStatusCheckCVL() expect void;
    
    function _.requireAccountAndVaultStatusCheck(address caller) external 
        => requireVaultAccountStatusCheckCVL(caller) expect void;
    
    function _.getCurrentOnBehalfOfAccount(address controllerToCheck) external 
        => getCurrentOnBehalfOfAccountCVL(controllerToCheck) expect (address, bool) ALL;
    
    function _.getLastAccountStatusCheckTimestamp(address account) external with (env e)
        => getLastAccountStatusCheckTimestampCVL(e, account) expect uint256 ALL;

    function _.getAccountOwner(address account) external
        => getAccountOwnerCVL(account) expect address ALL;

    function _.isControlCollateralInProgress() external 
        => isControlCollateralInProgressCVL() expect bool ALL;

    function _.areChecksInProgress() external => NONDET;
    function _.disableController(address account) external => NONDET;
    function _.isOperatorAuthenticated() external => NONDET;
    function _.controlCollateral(address targetCollateral, address onBehalfOfAccount, uint256 value, bytes) external => NONDET;
    function _.forgiveAccountStatusCheck(address account) external => NONDET;
    function _.getControllers(address account) external => NONDET;
    function _.getCollaterals(address account) external => NONDET;
    function _.isCollateralEnabled(address account, address vault) external => NONDET;
    function _.isAccountStatusCheckDeferred(address account) external => NONDET;
    function _.isVaultStatusCheckDeferred(address vault) external => NONDET;
    function _.isControllerEnabled(address account, address vault) external => NONDET;

    //
    // SequenceRegistry
    //

    function _.reserveSeqId(string) external => NONDET;
}

// Governor is guaranteed that the protocol fee share will not exceed this value (0.5e4)
definition MAX_PROTOCOL_FEE_SHARE() returns mathint = 5 * 10^3;

// max interest rate accepted from IRM. 1,000,000% APY: floor(((1000000 / 100 + 1)**(1/(86400*365.2425)) - 1) * 1e27)
definition MAX_ALLOWED_INTEREST_RATE() returns mathint = 291867278914945094175;

definition INTEREST_ACCUMULATOR_SCALE() returns mathint = 10^27;

definition CONFIG_SCALE() returns mathint = 10^4;
definition MAX_SANE_AMOUNT() returns mathint = max_uint112;

definition INTERNAL_DEBT_PRECISION_SHIFT() returns uint256 = 31;
definition MAX_SANE_DEBT_AMOUNT() returns mathint = require_uint256(MAX_SANE_AMOUNT()) << INTERNAL_DEBT_PRECISION_SHIFT();

definition OP_MAX_VALUE() returns mathint = 1<<15;
definition CFG_MAX_VALUE() returns mathint = 1<<2;

definition CHECKACCOUNT_NONE() returns address = 0;
definition CHECKACCOUNT_CALLER() returns address = 1;

definition TIMESTAMP_3000_YEAR() returns mathint = 32499081600;

definition OWED_MASK() returns uint256 = 0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF0000000000000000000000000000;
definition OWED_OFFSET() returns uint256 = 112;
definition OWED_FROM_DATA(uint256 data) returns uint256 = (data & OWED_MASK()) >> OWED_OFFSET();

function requireValidTimeStamp(env e) {
    require(e.block.timestamp > 0);
    // There is a safe accumption limit timestamp to 3000 year
    require(to_mathint(e.block.timestamp) < TIMESTAMP_3000_YEAR());
}

function requireValidTimeStampInv(env eInv, env e) {
    require(eInv.block.timestamp == e.block.timestamp);
    requireValidTimeStamp(e);
}

ghost CVLGetQuote(uint256, address, address) returns uint256 {
    // The total value returned by the oracle is assumed < 2**230-1.
    // There will be overflows without an upper bound on this number.
    // (For example, it must be less than 2**242-1 to avoid overflow in
    // LTVConfig.mul)
    axiom forall uint256 x. forall address y. forall address z. 
        CVLGetQuote(x, y, z) < 1725436586697640946858688965569256363112777243042596638790631055949823;
}

function CVLGetQuotes(uint256 amount, address base, address quote) returns (uint256, uint256) {
    return (
        CVLGetQuote(amount, base, quote),
        CVLGetQuote(amount, base, quote)
    );
}

persistent ghost bool ghostIsControlCollateralInProgress;
function isControlCollateralInProgressCVL() returns bool {
    return ghostIsControlCollateralInProgress;
}

persistent ghost bool ghostBalanceTrackerHookCalled;
persistent ghost address ghostBalanceTrackerHookAccount;
persistent ghost mathint ghostBalanceTrackerHookBalance;
persistent ghost bool ghostBalanceTrackerHookForfeit;
function balanceTrackerHookCVL(address account, uint256 newAccountBalance, bool forfeitRecentReward) {
    ghostBalanceTrackerHookCalled = true;
    ghostBalanceTrackerHookAccount = account;
    ghostBalanceTrackerHookBalance = newAccountBalance;
    ghostBalanceTrackerHookForfeit = forfeitRecentReward;
}

persistent ghost mapping(address => mapping(uint256 => mapping(uint256 => uint256))) ghostComputedInterestRate;
persistent ghost address ghostComputeInterestRateVault;
function computeInterestRateCVL(address vault, uint256 cash, uint256 borrows) returns uint256 {
    ghostComputeInterestRateVault = vault;
    return ghostComputedInterestRate[vault][cash][borrows];
}

persistent ghost bool ghostProtocolFeeConfigCalled;
persistent ghost address ghostProtocolFeeRequestedVault {
    init_state axiom ghostProtocolFeeRequestedVault == currentContract;
}
persistent ghost mapping(address => address) ghostProtocolFeeReceiver;
persistent ghost mapping(address => uint16) ghostProtocolFeeShare;
function protocolFeeConfigCVL(address vault) returns (address, uint16) {
    ghostProtocolFeeConfigCalled = true;
    ghostProtocolFeeRequestedVault = vault;
    return (ghostProtocolFeeReceiver[vault], ghostProtocolFeeShare[vault]);
}

persistent ghost mathint ghostLogVaultInterestRate;
function logVaultStatusCVL(uint256 interestRate) {
    ghostLogVaultInterestRate = interestRate;
}

persistent ghost address ghostOnBehalfOfAccount;
persistent ghost bool ghostControllerEnabled;
function getCurrentOnBehalfOfAccountCVL(address controllerToCheck) returns (address, bool) {
    // for safety, EVC reverts if no account has been authenticated
    require(ghostOnBehalfOfAccount != 0);
    require(ghostOnBehalfOfAccount != currentContract);
    require(controllerToCheck == 0 => ghostControllerEnabled == false);
    return (ghostOnBehalfOfAccount, ghostControllerEnabled);
}

persistent ghost mathint ghostLastAccountStatusCheckTimestamp;
function getLastAccountStatusCheckTimestampCVL(env e, address account) returns uint256 {
    require(ghostLastAccountStatusCheckTimestamp <= to_mathint(e.block.timestamp));
    return require_uint256(ghostLastAccountStatusCheckTimestamp);
}
 
persistent ghost mapping (address => address) ghostAccountOwner;
function getAccountOwnerCVL(address account) returns address {
    return ghostAccountOwner[account];
}

persistent ghost bool ghostRequireVaultStatusCheckCalled;
function requireVaultStatusCheckCVL() {
    ghostRequireVaultStatusCheckCalled = true;
}

persistent ghost address ghostRequireVaultAccountStatusCheckCaller;
persistent ghost bool ghostRequireVaultAccountStatusCheckCalled;
function requireVaultAccountStatusCheckCVL(address caller) {
    ghostRequireVaultAccountStatusCheckCalled = true;
    ghostRequireVaultAccountStatusCheckCaller = caller;
    assert(caller != CHECKACCOUNT_CALLER());
}

function reentrantViewSenderRequirementCVL(env e) {
    // The hook target is allowed to bypass the RO-reentrancy lock. The hook target can either be a msg.sender
    // when the view function is inlined in the EVault.sol or the hook target should be taken from the trailing
    // data appended by the delegateToModuleView function used by useView modifier. In the latter case, it is
    // safe to consume the trailing data as we know we are inside useView because msg.sender == address(this)
    require(e.msg.sender != ghostHookTarget);
    require(e.msg.sender != currentContract);
}

// Summarize trySafeTransferFrom as DummyERC20 transferFrom
function trySafeTransferFromCVL(env e, address from, address to, uint256 value) returns (bool, bytes) {
    bytes ret; // Ideally bytes("") if there is a way to do this
    return (_Asset.transferFrom(e, from, to, value), ret);
}

persistent ghost address ghostOracleAddress;
persistent ghost address ghostUnitOfAccount;
function metadataCVL() returns (address, address, address) {
    require(ghostOracleAddress != _Asset);
    require(ghostOracleAddress != ghostUnitOfAccount);
    return (_Asset, ghostOracleAddress, ghostUnitOfAccount);
}

function CVLMulDiv(uint144 a, uint256 b, uint256 c) returns uint144 {
    mathint result = (a * b) / c; 
    require result <= max_uint144;
    return assert_uint144(result); 
}

persistent ghost mapping(address => bool) ghostAnyControllerEnabled;
function hasAnyControllerEnabledCVL(address caller) returns bool {
    return ghostAnyControllerEnabled[caller];
}