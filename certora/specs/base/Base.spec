import "./RPow.spec";
import "./LoadVault.spec";
import "../methods/BaseMethods.spec";

using DummyERC20A as _ERC20A;

methods {

    //
    // Internal
    //
    
    // Resolve asset to DummyERC20A
    function ProxyUtils.metadata() internal => metadataCVL() expect (address, address, address) ALL;

    function _.mulDiv(uint144 a, uint256 b, uint256 c) internal => CVLMulDiv(a, b, c) expect uint144;

    function _.trySafeTransferFrom(address token, address from, address to, uint256 value) internal with (env e) 
        => trySafeTransferFromCVL(e, from, to, value) expect (bool, bytes memory);
    function _.safeTransferFrom(address token, address from, address to, uint256 value, address permit2) internal with (env e)
        => trySafeTransferFromCVL(e, from, to, value) expect (bool, bytes memory);

    function RPow.rpow(uint256 x, uint256 y, uint256 base) internal returns (uint256, bool) => CVLPow(x, y, base);

    function _.logVaultStatus(GovernanceHarness.VaultCache memory a, uint256 interestRate) internal 
        => logVaultStatusCVL(interestRate) expect void;

    function Cache.loadVault() internal returns (VaultHarness.VaultCache memory) with (env e) 
        => loadVaultAssumeNoUpdateCVL(e);

    function _.invokeHookTarget(address caller) internal => NONDET;
    function _.calculateDTokenAddress() internal => NONDET;

    //
    // DToken
    // 

    function _.emitTransfer(address, address, uint256) external => NONDET;

    //
    // BalanceForwarder
    //

    function _.balanceTrackerHook(address account, uint256 newAccountBalance, bool forfeitRecentReward) external => NONDET;

    //
    // PriceOracle
    //

    function _.getQuote(uint256 amount, address base, address quote) external 
        => getQuoteCVL(amount, base, quote) expect (uint256);
    function _.getQuotes(uint256 amount, address base, address quote) external 
        => getQuotesCVL(amount, base, quote) expect (uint256, uint256);

    //
    // ProtocolConfig
    //

    function _.protocolFeeConfig(address vault) external 
        => protocolFeeConfigCVL(vault) expect (address, uint16) ALL;

    //
    // IRM
    //

    function _.computeInterestRate(address, uint256, uint256) external => NONDET;
    function _.computeInterestRateView(address, uint256, uint256) external => NONDET;

    //
    // Asset
    //
    
	function _.name() external => DISPATCHER(true);
    function _.symbol() external => DISPATCHER(true);
    function _.decimals() external => DISPATCHER(true);
    function _.totalSupply() external => DISPATCHER(true);
    function _.balanceOf(address) external => DISPATCHER(true);
    function _.allowance(address,address) external => DISPATCHER(true);
    function _.approve(address,uint256) external => DISPATCHER(true);
    function _.transfer(address,uint256) external => DISPATCHER(true);
    function _.transferFrom(address,address,uint256) external => DISPATCHER(true);

    //
    // EVC
    //

    function _.requireVaultStatusCheck() external 
        => requireVaultStatusCheckCVL() expect void;
    function _.requireAccountAndVaultStatusCheck(address caller) external 
        => requireVaultAccountStatusCheckCVL(caller) expect void;
    function _.getCurrentOnBehalfOfAccount(address controllerToCheck) external 
        => getCurrentOnBehalfOfAccountCVL(controllerToCheck) expect (address, bool) ALL;

    function _.areChecksInProgress() external => NONDET;
    function _.disableController(address) external => NONDET;
    function _.isOperatorAuthenticated() external => NONDET;
    function _.isControlCollateralInProgress() external => NONDET;
    function _.getAccountOwner(address) external => NONDET;
    function _.controlCollateral(address, address, uint256, bytes) external => NONDET;
    function _.forgiveAccountStatusCheck(address) external => NONDET;
    function _.getControllers(address) external => NONDET;
    function _.getCollaterals(address) external => NONDET;
    function _.isCollateralEnabled(address, address) external => NONDET;
    function _.isAccountStatusCheckDeferred(address) external => NONDET;
    function _.isVaultStatusCheckDeferred(address) external => NONDET;
    function _.getLastAccountStatusCheckTimestamp(address) external => NONDET;
}

definition CONFIG_SCALE() returns mathint = 10^4;

definition CHECKACCOUNT_NONE() returns address = 0;
definition CHECKACCOUNT_CALLER() returns address = 1;

////////////////// FUNCTIONS //////////////////////

persistent ghost bool ghostProtocolFeeConfigCalled;
persistent ghost address ghostProtocolFeeRequestedVault {
    init_state axiom ghostProtocolFeeRequestedVault == currentContract;
}
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
    return (ghostOnBehalfOfAccount, controllerToCheck == 0 => ghostControllerEnabled == false);
}

persistent ghost bool ghostRequireVaultStatusCheckCalled;
function requireVaultStatusCheckCVL() {
    ghostRequireVaultStatusCheckCalled = true;
}

persistent ghost bool ghostRequireVaultAccountStatusCheckCalled;
function requireVaultAccountStatusCheckCVL(address caller) {
    ghostRequireVaultAccountStatusCheckCalled = true;
    assert(caller != CHECKACCOUNT_CALLER());
}

function reentrantViewSenderRequirementCVL(env e) {
    // The hook target is allowed to bypass the RO-reentrancy lock. The hook target can either be a msg.sender
    // when the view function is inlined in the EVault.sol or the hook target should be taken from the trailing
    // data appended by the delegateToModuleView function used by useView modifier. In the latter case, it is
    // safe to consume the trailing data as we know we are inside useView because msg.sender == address(this)
    require(e.msg.sender != hookTarget());
    require(e.msg.sender != currentContract);
}

// Summarize trySafeTransferFrom as DummyERC20 transferFrom
function trySafeTransferFromCVL(env e, address from, address to, uint256 value) returns (bool, bytes) {
    bytes ret; // Ideally bytes("") if there is a way to do this
    return (_ERC20A.transferFrom(e, from, to, value), ret);
}

persistent ghost address ghostOracleAddress;
persistent ghost address ghostUnitOfAccount;
function metadataCVL() returns (address, address, address) {
    require(ghostOracleAddress != _ERC20A);
    require(ghostOracleAddress != ghostUnitOfAccount);
    return (_ERC20A, ghostOracleAddress, ghostUnitOfAccount);
}

function CVLMulDiv(uint144 a, uint256 b, uint256 c) returns uint144 {
    mathint result = (a * b) / c; 
    require result <= max_uint144;
    return assert_uint144(result); 
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

///////////////// GHOSTS & HOOKS //////////////////

persistent ghost mapping(address => address) ghostProtocolFeeReceiver;
persistent ghost mapping(address => uint16) ghostProtocolFeeShare;

//
// ltvLookup[].interestRate
//

persistent ghost mathint ghostInterestRate {
    init_state axiom ghostInterestRate == 0;
}

hook Sload uint72 val currentContract.vaultStorage.interestRate {
    require(require_uint72(ghostInterestRate) == val);
} 

hook Sstore currentContract.vaultStorage.interestRate uint72 val {
    ghostInterestRate = val;
}

//
// vaultStorage.ltvList
//

persistent ghost mapping (mathint => address) ghostLTVList {
    init_state axiom forall mathint i. forall mathint j. ghostLTVList[i] != ghostLTVList[j];
}

hook Sload address val currentContract.vaultStorage.ltvList[INDEX uint256 i] {
    require(ghostLTVList[i] == val);
} 

hook Sstore currentContract.vaultStorage.ltvList[INDEX uint256 i] address val {
    ghostLTVList[i] = val;
}

//
// ltvLookup[].borrowLTV
//

persistent ghost mapping (address => mathint) ghostBorrowLTV {
    init_state axiom forall address i. ghostBorrowLTV[i] == 0;
}

hook Sload GovernanceHarness.ConfigAmount val currentContract.vaultStorage.ltvLookup[KEY address i].borrowLTV {
    require(require_uint16(ghostBorrowLTV[i]) == val);
} 

hook Sstore currentContract.vaultStorage.ltvLookup[KEY address i].borrowLTV GovernanceHarness.ConfigAmount val {
    ghostBorrowLTV[i] = val;
}

//
// ltvLookup[].liquidationLTV
//

persistent ghost mapping (address => mathint) ghostLiquidationLTV {
    init_state axiom forall address i. ghostLiquidationLTV[i] == 0;
}

persistent ghost mapping (address => mathint) ghostLiquidationLTVPrev {
    init_state axiom forall address i. ghostLiquidationLTVPrev[i] == 0;
}

hook Sload GovernanceHarness.ConfigAmount val currentContract.vaultStorage.ltvLookup[KEY address i].liquidationLTV {
    require(require_uint16(ghostLiquidationLTV[i]) == val);
} 

hook Sstore currentContract.vaultStorage.ltvLookup[KEY address i].liquidationLTV GovernanceHarness.ConfigAmount val {
    ghostLiquidationLTVPrev[i] = ghostLiquidationLTV[i];
    ghostLiquidationLTV[i] = val;
}

//
// ltvLookup[].initialLiquidationLTV
//

persistent ghost mapping (address => mathint) ghostInitialLiquidationLTV {
    init_state axiom forall address i. ghostInitialLiquidationLTV[i] == 0;
}

hook Sload GovernanceHarness.ConfigAmount val currentContract.vaultStorage.ltvLookup[KEY address i].initialLiquidationLTV {
    require(require_uint16(ghostInitialLiquidationLTV[i]) == val);
} 

hook Sstore currentContract.vaultStorage.ltvLookup[KEY address i].initialLiquidationLTV GovernanceHarness.ConfigAmount val {
    ghostInitialLiquidationLTV[i] = val;
}

//
// ltvLookup[].targetTimestamp
//

persistent ghost mapping (address => uint48) ghostLtvTargetTimestamp {
    init_state axiom forall address i. ghostLtvTargetTimestamp[i] == 0;
}

hook Sload uint48 val currentContract.vaultStorage.ltvLookup[KEY address i].targetTimestamp {
    require(ghostLtvTargetTimestamp[i] == val);
} 

hook Sstore currentContract.vaultStorage.ltvLookup[KEY address i].targetTimestamp uint48 val {
    ghostLtvTargetTimestamp[i] = val;
}

//
// ltvLookup[].rampDuration
//

persistent ghost mapping (address => mathint) ghostLtvRampDuration {
    init_state axiom forall address i. ghostLtvRampDuration[i] == 0;
}

persistent ghost mapping (address => mathint) ghostLtvRampDurationPrev {
    init_state axiom forall address i. ghostLtvRampDurationPrev[i] == 0;
}

hook Sload uint32 val currentContract.vaultStorage.ltvLookup[KEY address i].rampDuration {
    require(require_uint32(ghostLtvRampDuration[i]) == val);
} 

hook Sstore currentContract.vaultStorage.ltvLookup[KEY address i].rampDuration uint32 val {
    ghostLtvRampDurationPrev[i] = ghostLtvRampDuration[i];
    ghostLtvRampDuration[i] = val;
}

//
// ltvLookup[].initialized
//

persistent ghost mapping (address => bool) ghostLtvInitialized {
    init_state axiom forall address i. ghostLtvInitialized[i] == false;
}

hook Sload bool val currentContract.vaultStorage.ltvLookup[KEY address i].initialized {
    require(ghostLtvInitialized[i] == val);
} 

hook Sstore currentContract.vaultStorage.ltvLookup[KEY address i].initialized bool val {
    ghostLtvInitialized[i] = val;
}

///////////////// PROPERTIES //////////////////////

rule specificFunctionsModifyState(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_METHODS(f) } {
    
    storage before = lastStorage;

    f(e, args);

    storage after = lastStorage;

    assert(before[currentContract] != after[currentContract] => MODIFY_STATE_METHODS(f));
}

rule modifyStatePossibility(env e, method f, calldataarg args) 
    filtered { f -> MODIFY_STATE_METHODS(f) } {
    
    storage before = lastStorage;

    f(e, args);

    storage after = lastStorage;

    satisfy(before[currentContract] != after[currentContract]);
}

rule stateChangeFunctionsReentrancyProtected(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_METHODS(f) } {

    bool locked = reentrancyLocked();

    storage before = lastStorage;

    f(e, args);

    storage after = lastStorage;

    assert(before[currentContract] != after[currentContract] => !locked);
}

rule notAbleReceiveNativeTokens(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_METHODS(f) } {

    f@withrevert(e, args);

    assert(e.msg.value != 0 => lastReverted);
}

rule anyoneCanExecuteViewFunctions(env e1, env e2, method f, calldataarg args) 
    filtered { f -> f.isView && !HARNESS_METHODS(f) } {

    reentrantViewSenderRequirementCVL(e1);
    reentrantViewSenderRequirementCVL(e2);

    require(e1.msg.value == e2.msg.value);
    require(e1.block.timestamp == e2.block.timestamp);

    require(e1.msg.sender != e2.msg.sender);

    storage init = lastStorage;

    f@withrevert(e1, args) at init;
    bool reverted1 = lastReverted;

    f@withrevert(e2, args) at init;
    bool reverted2 = lastReverted;

    // Sender address should not affect to functions execution
    assert(reverted1 == reverted2);
} 

rule viewFunctionsNotProtectedAgainstReentrancy(env e, method f, calldataarg args) 
    filtered { f -> f.isView  && !HARNESS_METHODS(f) } {

    reentrantViewSenderRequirementCVL(e);

    require(reentrancyLocked());

    f@withrevert(e, args);

    // Function could be executed when reentrancy in locked state
    satisfy(!lastReverted);
}

rule specificViewFunctionsProtectedAgainstReentrancy(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_METHODS(f) } {

    reentrantViewSenderRequirementCVL(e);

    require(reentrancyLocked());

    f@withrevert(e, args);
    bool reverted = lastReverted;

    // MUST revert
    assert(VIEW_REENTRANCY_PROTECTED_METHODS(f) => reverted);

    // Possibility not been reverted
    satisfy(f.isView && !VIEW_REENTRANCY_PROTECTED_METHODS(f) => !reverted);
}

rule viewFunctionsDontUpdateState(env e, method f, calldataarg args) 
    filtered { f -> VIEW_METHODS(f) } {

    storage before = lastStorage;

    f(e, args);

    storage after = lastStorage;

    assert(before[currentContract] == after[currentContract]);
}