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
use invariant totalSharesBorrowsFeeLimits;
use invariant validateNotUseZeroAddress;
use invariant noSelfCollateralization;
use invariant uniqueLTVEntries;
use invariant lastInterestAccumulatorNotInFuture;
use invariant timestampSetWhenPositiveAccumulatedFees;
use invariant borrowLTVLowerOrEqualLiquidationLTV;
use invariant initializedLTVWhenSet;
use invariant zeroTimestampInitializedSolvency;
use invariant LTVTimestampValid;
use invariant LTVTimestampFutureRamping;
use invariant initializedLTVInCollateralList;
use invariant zeroTimestampIndicatesLTVCleared;
use invariant configParamsScaledTo1e4;
use invariant ltvFractionScaled;
use invariant LTVLiquidationDynamic;
use invariant LTVRampingTimeWithinBounds;

// Functions are not able to receive native tokens
use rule notAbleReceiveNativeTokens;

definition HARNESS_METHODS(method f) returns bool = BASE_HARNESS_METHODS(f);

// @todo Snapshot is disabled if both caps are disabled (at low-level set to 0, but resolved to max_uint256)
invariant snapshotDisabledWithBothCapsDisabled() 
    ghostSupplyCap == 0 && ghostBorrowCap == 0 => ghostSnapshotInitialized == false
    filtered { f -> !HARNESS_METHODS(f) }


// Snapshot MUST NOT be used when it is not initialized
rule snapshotUsedWhenInitialized(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_METHODS(f) } {

    mathint snapshotCashPrev = ghostSnapshotCash;
    mathint snapshotBorrows = ghostSnapshotBorrows;

    f(e, args);

    assert((ghostSnapshotCash != 0 && ghostSnapshotBorrows != 0)
        && (snapshotCashPrev != ghostSnapshotCash || snapshotBorrows != ghostSnapshotBorrows) 
        => ghostSnapshotInitialized == true
        );
}

// Snapshot cash MUST set from storage cash or reset
rule snapshotCashSetFromStorage(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_METHODS(f) } {

    requireInvariant uninitializedSnapshotReset;
    requireInvariant snapshotDisabledWithBothCapsDisabled;

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

// Clearing accumulated fees must move the fees to one or two designated fee receiver addresses
rule feesClearedToReceivers(env e, method f, calldataarg args, address user1, address user2) 
    filtered { f -> !HARNESS_METHODS(f) } {

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

// Accumulated fees must result in an increase in the total shares of the vault
rule accumulatedFeesIncreaseTotalShares(env e) {

    mathint accumulatedFeesPrev = ghostAccumulatedFees;
    mathint totalSharesPrev = ghostTotalShares;

    touchHarness(e);
    
    assert(ghostAccumulatedFees >= accumulatedFeesPrev 
        => (ghostTotalShares - totalSharesPrev == ghostAccumulatedFees - accumulatedFeesPrev)
    );
}

// Change accumulated fees accrued MUST set last interest accumulator timestamp
rule interestFeesAccruedSetTimestamp(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_METHODS(f) } {
    
    requireInvariant lastInterestAccumulatorNotInFuture(e);

    mathint accumulatedFeesPrev = ghostAccumulatedFees;

    f(e, args);
    
    assert(accumulatedFeesPrev != ghostAccumulatedFees
        => ghostLastInterestAccumulatorUpdate == to_mathint(e.block.timestamp)
    );
}

// @todo Accumulated fees and interest accumulator are updated only when time has passed since the last update
rule feesAndInterestNotUpdateNoTimePassed(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_METHODS(f) } {

    require(e.block.timestamp > 0);

    mathint interestAccumulatorPrev = ghostInterestAccumulator;
    mathint accumulatedFeesPrev = ghostAccumulatedFees;

    f(e, args);

    assert(ghostLastInterestAccumulatorUpdate == to_mathint(e.block.timestamp) 
        => (interestAccumulatorPrev == ghostInterestAccumulator && accumulatedFeesPrev == ghostAccumulatedFees)
    );
}

// The vault's cash changes without assets transfer only when surplus assets available
rule cashChangesSkim(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_METHODS(f) } {

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

// Transferring assets from the vault MUST decrease the available cash balance
rule transferOutDecreaseCash(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_METHODS(f) } {

    requireInvariant cashNotLessThanAssets;

    mathint cashPrev = ghostCash;
    mathint erc20BalancePrev = ghostErc20Balances[currentContract];

    f(e, args);

    assert(erc20BalancePrev > ghostErc20Balances[currentContract]
        => (erc20BalancePrev - ghostErc20Balances[currentContract] == cashPrev - ghostCash)
    );
}

// Changes in the cash balance must correspond to changes in the total shares
rule cashChangesAffectTotalShares(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_METHODS(f) } {

    mathint cashPrev = ghostCash;
    mathint totalSharesPrev = ghostTotalShares;

    f(e, args);

    assert(cashPrev != ghostCash => totalSharesPrev != ghostTotalShares);
}

// Accumulated fees must not decrease unless they are being reset to zero
rule accumulatedFeesNonDecreasing(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_METHODS(f) } {

    mathint accumulatedFeesPrev = ghostAccumulatedFees;

    f(e, args);
    
    assert(ghostAccumulatedFees == 0 || ghostAccumulatedFees >= accumulatedFeesPrev);
}

// Fees are retrieved only for the contract itself from the protocol config contract
invariant feesRetrievedForCurrentContract(env e) ghostProtocolFeeRequestedVault == currentContract
    filtered { f -> !HARNESS_METHODS(f) }

// Ramp duration can be used only when lowering liquidation LTV
rule rampDurationOnlyWhenLoweringLiquidationLTV(env e, method f, calldataarg args, address collateral)
    filtered { f -> !HARNESS_METHODS(f) } {
    
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

// Collateral LTV MUST NOT be removed completely
rule collateralLTVNotRemoved(env e, method f, calldataarg args, address collateral) 
    filtered { f -> !HARNESS_METHODS(f) } {

    bool initialized = ghostLtvInitialized[collateral];

    f(e, args);

    assert(initialized => ghostLtvInitialized[collateral]);
}