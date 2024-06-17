import "./base/Base.spec";
import "./common/State.spec";
import "./common/Funcs.spec";

// Valid state invariants
use invariant vaultNotDeinitialized;
use invariant uninitializedSnapshotReset;
use invariant snapshotStampAlwaysOne;
use invariant cashNotLessThanAssets;
use invariant supplyBorrowCapsLimits;
use invariant hooksLimits;
use invariant accumulatedFeesLimits;
use invariant validateNotUseZeroAddress;
use invariant noSelfCollateralization;
use invariant uniqueLTVEntries;
use invariant lastInterestAccumulatorNotInFuture;
use invariant timestampSetWhenPositiveAccumulatedFees;
use invariant borrowLTVLowerOrEqualLiquidationLTV;
use invariant initializedLTVWhenSet;
use invariant zeroTimestampInitializedSolvency;
use invariant ltvTimestampValid;
use invariant ltvTimestampFutureRamping;
use invariant initializedLTVInCollateralList;
use invariant zeroTimestampIndicatesLTVCleared;
use invariant configParamsScaledTo1e4;
use invariant ltvFractionScaled;
use invariant ltvLiquidationDynamic;
use invariant ltvRampingTimeWithinBounds;
use invariant configFlagsLimits;
use invariant transferNotAllowedToZeroAddress;
use invariant userInterestAccumulatorLeqVault;
use invariant userInterestAccumulatorSetWithNonZeroOwed;
use invariant interestAccumulatorScaledBy1e27;
use invariant interestRateZeroWithoutModel;
use invariant interestRateMaxLimit;
use invariant differentOwnerAndSpenderAllowances;

definition HARNESS_METHODS(method f) returns bool = BASE_HARNESS_METHODS(f);

// COM-01 | Accumulated fees must result in an increase in the total shares of the vault
rule accumulatedFeesIncreaseTotalShares(env e) {

    mathint accumulatedFeesPrev = ghostAccumulatedFees;
    mathint totalSharesPrev = ghostTotalShares;

    touchHarness(e);
    
    assert(ghostTotalShares - totalSharesPrev == ghostAccumulatedFees - accumulatedFeesPrev);
}

// COM-02 | Snapshot MUST NOT be used when it is not initialized
rule snapshotUsedWhenInitialized(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    mathint snapshotCashPrev = ghostSnapshotCash;
    mathint snapshotBorrows = ghostSnapshotBorrows;

    f(e, args);

    assert((ghostSnapshotCash != 0 && ghostSnapshotBorrows != 0)
        && (snapshotCashPrev != ghostSnapshotCash || snapshotBorrows != ghostSnapshotBorrows) 
        => ghostSnapshotInitialized == true
        );
}

// COM-03 | Snapshot cash MUST set from storage cash or reset
rule snapshotCashSetFromStorage(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    requireInvariant uninitializedSnapshotReset;

    bool initialized = ghostSnapshotInitialized;
    mathint cashPrev = ghostCash;

    f(e, args);

    // Cash in snapshot was changed
    assert(ghostSnapshotInitialized && initialized != ghostSnapshotInitialized
        => (ghostCash == cashPrev
            // Cash in storage was NOT changed in this transaction
            ? ghostSnapshotCash == ghostCash
            // Cash in storage was changed after been saved in cache
            : ghostSnapshotCash == cashPrev
            )
    );
}

// COM-04 | Clearing accumulated fees must move the fees to one or two designated fee receiver addresses
rule feesClearedToReceivers(env e, method f, calldataarg args, address user1, address user2) 
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    require(user1 != user2);

    mathint accumulatedFeesPrev = ghostAccumulatedFees;
    mathint balanceFirstReceiverPrev = ghostUsersDataBalance[user1];
    mathint balanceSecondReceiverPrev = ghostUsersDataBalance[user2];

    f(e, args);
    
    // Accumulated fees were cleared
    satisfy(ghostAccumulatedFees == 0 && ghostAccumulatedFees != accumulatedFeesPrev
        => (ghostUsersDataBalance[user1] > balanceFirstReceiverPrev
            && ghostUsersDataBalance[user2] > balanceSecondReceiverPrev
        )
    );
}

// COM-05 | Functions are not able to receive native tokens
use rule notAbleReceiveNativeTokens;

// COM-06 | Change interest accumulator or accumulated fees accrued MUST set last interest accumulator timestamp
rule interestFeesAccruedSetTimestamp(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {
    
    requireInvariant lastInterestAccumulatorNotInFuture(e);
    requireValidTimeStamp(e);

    mathint interestAccumulatorPrev = ghostInterestAccumulator;
    mathint accumulatedFeesPrev = ghostAccumulatedFees;

    f(e, args);
    
    assert(interestAccumulatorPrev != ghostInterestAccumulator || accumulatedFeesPrev != ghostAccumulatedFees
        => ghostLastInterestAccumulatorUpdate == to_mathint(e.block.timestamp)
    );
}

// COM-07 | Interest accumulator is updated only when last interest accumulator time changed
rule feesAndInterestNotUpdateNoAccumulatorUpdate(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    mathint lastInterestAccumulatorUpdatePrev = ghostLastInterestAccumulatorUpdate;
    mathint interestAccumulatorPrev = ghostInterestAccumulator;

    f(e, args);

    assert(lastInterestAccumulatorUpdatePrev == ghostLastInterestAccumulatorUpdate 
        => interestAccumulatorPrev == ghostInterestAccumulator
    );
}

// COM-08 | The vault's cash changes without assets transfer only when surplus assets available
rule cashChangesSkim(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    requireInvariant cashNotLessThanAssets;

    mathint cashPrev = ghostCash;
    mathint erc20BalancePrev = ghostErc20Balances[currentContract];

    f(e, args);

    // Cashed changes without assets transfer
    assert(ghostCash > cashPrev && ghostErc20Balances[currentContract] == erc20BalancePrev
            // Only when was a surplus of assets
        => (erc20BalancePrev > cashPrev
            // Cash MUST NOT increase more than was available surplus
            && erc20BalancePrev - cashPrev >= ghostCash - cashPrev
        )
    );
}

// COM-09 | Transferring assets from the vault MUST decrease the available cash balance
rule transferOutDecreaseCash(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    requireInvariant cashNotLessThanAssets;

    mathint cashPrev = ghostCash;
    mathint erc20BalancePrev = ghostErc20Balances[currentContract];

    f(e, args);

    assert(erc20BalancePrev > ghostErc20Balances[currentContract]
        => (erc20BalancePrev - ghostErc20Balances[currentContract] == cashPrev - ghostCash)
    );
}

// COM-10 | Changes in the cash balance must correspond to changes in the total shares
rule cashChangesAffectTotalShares(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    mathint cashPrev = ghostCash;
    mathint totalSharesPrev = ghostTotalShares;

    f(e, args);

    assert(cashPrev != ghostCash => totalSharesPrev != ghostTotalShares);
}

// COM-11 | Accumulated fees must not decrease unless they are being reset to zero
rule accumulatedFeesNonDecreasing(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    mathint accumulatedFeesPrev = ghostAccumulatedFees;

    f(e, args);
    
    assert(ghostAccumulatedFees == 0 || ghostAccumulatedFees >= accumulatedFeesPrev);
}

// COM-12 | Fees are retrieved only for the contract itself from the protocol config contract
invariant feesRetrievedForCurrentContract(env e) ghostProtocolFeeRequestedVault == currentContract
    filtered { f -> !HARNESS_VIEW_METHODS(f) }

// COM-13 | Ramp duration can be used only when lowering liquidation LTV
rule rampDurationOnlyWhenLoweringLiquidationLTV(env e, method f, calldataarg args, address collateral)
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {
    
    uint16 borrowLTV;
    uint16 liquidationLTV;
    uint16 initialLiquidationLTV;
    uint48 targetTimestamp;
    uint32 rampDuration;
    borrowLTV, liquidationLTV, initialLiquidationLTV, targetTimestamp, rampDuration = LTVFullHarness(collateral);
    
    liquidationLTV = getLiquidationLTV(e, collateral);

    f(e, args);

    uint16 _borrowLTV;
    uint16 _liquidationLTV;
    uint16 _initialLiquidationLTV;
    uint48 _targetTimestamp;
    uint32 _rampDuration;
    _borrowLTV, _liquidationLTV, _initialLiquidationLTV, _targetTimestamp, _rampDuration = LTVFullHarness(collateral);
        
    assert(rampDuration != _rampDuration && _rampDuration != 0 => _liquidationLTV < liquidationLTV);
}

// COM-14 | Collateral LTV MUST NOT be removed completely
rule collateralLTVNotRemoved(env e, method f, calldataarg args, address collateral) 
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    bool initialized = ghostLtvInitialized[collateral];

    f(e, args);

    assert(initialized => ghostLtvInitialized[collateral]);
}

// COM-15 | Interest accumulator always grows
rule interestAccumulatorAlwaysGrows(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    mathint interestAccumulatorPrev = ghostInterestAccumulator;

    f(e, args);

    assert(ghostInterestAccumulator >= interestAccumulatorPrev);
}

// COM-16 | User interest accumulator always grows
rule userInterestAccumulatorAlwaysGrows(env e, method f, calldataarg args, address user) 
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    mathint usersInterestAccumulatorPrev = ghostUsersInterestAccumulator[user];

    f(e, args);

    assert(ghostUsersInterestAccumulator[user] >= usersInterestAccumulatorPrev);
}

// COM-17 | User interest accumulator set always when user borrow changes
rule userInterestAccumulatorSetOnBorrowChange(env e, method f, calldataarg args, address user)
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    mathint userBorrowsPrev = getAccountOwed(user);
    mathint usersInterestAccumulatorPrev = ghostUsersInterestAccumulator[user];

    f(e, args);

    assert(userBorrowsPrev != to_mathint(getAccountOwed(user)) 
        ? ghostUsersInterestAccumulator[user] == ghostInterestAccumulator 
        : ghostUsersInterestAccumulator[user] == usersInterestAccumulatorPrev
        );
}

// COM-18 | Interest accumulator cannot overflow
rule interestAccumulatorCannotOverflow(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    requireValidStateEnvCVL(e);

    mathint interestAccumulatorPrev = ghostInterestAccumulator;

    uint256 x = require_uint256(ghostInterestRate + INTEREST_ACCUMULATOR_SCALE());
    uint256 n = require_uint256(e.block.timestamp - ghostLastInterestAccumulatorUpdate);
    uint256 scalar = require_uint256(INTEREST_ACCUMULATOR_SCALE());
    uint256 multiplier;
    bool overflow;
    multiplier, overflow = CVLPow(x, n, scalar);

    f(e, args);

    assert(overflow => interestAccumulatorPrev == ghostInterestAccumulator);
}

// COM-19 | Interest rate computed always for the current contract
rule interestRateForCurrentContract(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    address computeInterestRateVaultPrev = ghostComputeInterestRateVault;

    f(e, args);

    assert(computeInterestRateVaultPrev != ghostComputeInterestRateVault
        => ghostComputeInterestRateVault == currentContract
        );
}

// COM-20 | Transfer assets to sub-account allowed only when asset is compatible with EVC
rule transferAllowedOnlyWithCompatibleAsset(env e, method f, calldataarg args, address user) 
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    require(user != currentContract);

    mathint userAssetsBefore = ghostErc20Balances[user];

    f(e, args);

    // Sub-account balance can be changed only when asset is EVC compatible
    assert(userAssetsBefore < ghostErc20Balances[user] && isKnownNonOwnerAccountHarness(user)
        => evcCompatibleAsset() == true 
    );  

    // Sub-account balance MUST NOT increase when asset is not EVC compatible
    assert(isKnownNonOwnerAccountHarness(user) && evcCompatibleAsset() == false
        => userAssetsBefore >= ghostErc20Balances[user]
    );
}

// COM-21 | Creator is unchanged
rule creatorUnchanged(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    address creatorPrev = ghostCreator;

    f(e, args);

    assert(creatorPrev == ghostCreator);
}

// COM-22 | Accumulated fees unchanged when interest fees zero
rule accumulatedFeesUnchangedWhenInterestFeesZero(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    mathint interestFeePrev = ghostInterestFee;

    require(ghostAccumulatedFees == 0);
    require(ghostInterestFee == 0);

    f(e, args);

    // Interest fee was not changed and stays zero
    assert(interestFeePrev == ghostInterestFee
        // Accumulated fees stays zero
        => ghostAccumulatedFees == 0
    );
}

// COM-23 | Allowance unchanged when user redeem shares to their own account
rule allowanceUnchangedSelfWithdraw(env e, method f, calldataarg args, address from)
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    require(ghostAllowanceTouched == false);

    mathint fromBalancePrev = ghostUsersDataBalance[from];

    f(e, args);

    mathint fromBalancePost = ghostUsersDataBalance[from];

    // User withdraws assets to their own account
    assert(fromBalancePrev > fromBalancePost && from == ghostOnBehalfOfAccount
        => ghostAllowanceTouched == false
    );
}

// COM-24 | Allowance decrease (unless equal to max_uint256) when user redeem from another account
rule allowanceChangedFromAnotherWithdraw(env e, method f, calldataarg args, address from)
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    mathint fromBalancePrev = ghostUsersDataBalance[from];
    mathint usersETokenAllowancePrev = ghostUsersETokenAllowance[from][ghostOnBehalfOfAccount]; 

    f(e, args);

    mathint fromBalancePost = ghostUsersDataBalance[from];
    mathint usersETokenAllowancePost = ghostUsersETokenAllowance[from][ghostOnBehalfOfAccount]; 

    // Redeem shares to another account MUST decrease allowance, unless allowance is max_uint256
    assert(fromBalancePrev > fromBalancePost && from != ghostOnBehalfOfAccount
        => (usersETokenAllowancePrev == max_uint256
            ? usersETokenAllowancePrev == usersETokenAllowancePost
            : usersETokenAllowancePrev - usersETokenAllowancePost == fromBalancePrev - fromBalancePost
        )
    );
}

// COM-25 | Only the owner can increase allowance
rule onlyOwnerCanIncreaseAllowance(env e, method f, calldataarg args, address owner, address spender) 
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    mathint usersETokenAllowancePrev = ghostUsersETokenAllowance[owner][spender]; 

    f(e, args);

    mathint usersETokenAllowancePost = ghostUsersETokenAllowance[owner][spender]; 

    assert(usersETokenAllowancePost > usersETokenAllowancePrev
        => owner == e.msg.sender || owner == ghostOnBehalfOfAccount
    );
}

// COM-26 | Balance forwarder must be executed on any share movements when set
rule balanceForwarderExecutedOnShareMoves(env e, method f, calldataarg args, address account)
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {
    
    require(ghostBalanceTrackerHookCalled == false);

    bool enabled = isBalanceAndBalanceEnabled(account);
    mathint usersDataBalancePrev = ghostUsersDataBalance[account];

    f(e, args);

    mathint usersDataBalancePost = ghostUsersDataBalance[account];

    assert(enabled && usersDataBalancePrev != usersDataBalancePost
        => (ghostBalanceTrackerHookAccount == account 
            && ghostBalanceTrackerHookBalance == usersDataBalancePost
            && (usersDataBalancePost > usersDataBalancePrev 
                ? ghostBalanceTrackerHookForfeit == false
                : ghostBalanceTrackerHookForfeit == ghostIsControlCollateralInProgress
            )
        )
    );

    assert(ghostBalanceTrackerHookCalled => enabled);
}

// COM-27 | User borrow changes must be reflected in total borrows
rule userBorrowChangesInTotalBorrows(env e, method f, calldataarg args, address account)
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {
    
    mathint owedPrev = getAccountOwed(account);
    mathint totalBorrowsPrev = ghostTotalBorrows;

    f(e, args);

    mathint owedPost = getAccountOwed(account);

    assert(owedPrev != owedPost
        => (owedPrev > owedPost
            // Debt increased
            ? owedPost - owedPrev == ghostTotalBorrows - totalBorrowsPrev
            // Debt decreased
            : owedPrev - owedPost == totalBorrowsPrev - ghostTotalBorrows
        )
    );
}

// COM-28 | Increase or decrease user borrow transfers vault's assets out or in 
rule changeUserBorrowChangeVaultAssetBalance(env e, method f, calldataarg args, address account)
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    mathint owedPrev = getAccountOwed(account);
    mathint erc20BalancePrev = ghostErc20Balances[currentContract];

    f(e, args);

    mathint owedPost = getAccountOwed(account);
    mathint erc20BalancePost = ghostErc20Balances[currentContract];

    // Owed increased
    assert(owedPost != owedPrev
        => (owedPost > owedPrev
            ? erc20BalancePrev - erc20BalancePost == owedPost - owedPrev
            : erc20BalancePost - erc20BalancePrev == owedPrev - owedPost
        )
    );
}

// COM29 | Decrease shares or increase borrows MUST execute ACCOUNT health check
rule sharesDecreaseOrBorrowsIncreaseExecutesAccountHealthCheck(env e, method f, calldataarg args, address account) 
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    // Tested account != address(1)
    require(account != CHECKACCOUNT_CALLER());
    require(ghostRequireVaultAccountStatusCheckCaller == CHECKACCOUNT_CALLER());

    // Account owed before
    mathint owedPrev = getAccountOwed(account);
    // Account shares before
    mathint sharesPrev = ghostUsersDataBalance[account];

    // External contract call
    f(e, args);

    // Decrease shares or increase borrows
    assert(ghostUsersDataBalance[account] < sharesPrev || to_mathint(getAccountOwed(account)) > owedPrev
        // Vault health check was executed
        => ghostRequireVaultAccountStatusCheckCaller == account
    );
}

// COM30 | Increase shares or increase borrows MUST execute VAULT caps check
rule sharesIncreaseOrBorrowsIncreaseExecutesVaultHealthCheck(env e, method f, calldataarg args, address account) 
    filtered { f -> !HARNESS_VIEW_METHODS(f) } {

    // Tested account != address(1)
    require(account != CHECKACCOUNT_CALLER());
    require(ghostRequireVaultStatusCheckCalled == false);

    // Assets before
    mathint accountAssetsPrev = ghostErc20Balances[account];
    mathint vaultAssetsPrev = ghostErc20Balances[currentContract];

    // Account owed before
    mathint owedPrev = getAccountOwed(account);

    // Account shares before
    mathint sharesPrev = ghostUsersDataBalance[account];

    // External contract call
    f(e, args);

    // Increase shares or increase borrows
    assert((ghostUsersDataBalance[account] > sharesPrev || to_mathint(getAccountOwed(account)) > owedPrev)
        // There was not a transfer of shares from one user to another
        && accountAssetsPrev != ghostErc20Balances[account] && vaultAssetsPrev != ghostErc20Balances[currentContract]
        // Vault status check was executed
        => ghostRequireVaultStatusCheckCalled == true
    );
}