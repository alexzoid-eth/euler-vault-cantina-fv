import "./base/Base.spec";

function requireCommonCVL() {
}

// VS- | Vault MUST NOT be deinitialized
invariant vaultNotDeinitialized() 
    ghostInitialized == true;

// VS- | Uninitialized snapshot MUST be reset
invariant uninitializedSnapshotReset() 
    ghostSnapshotInitialized == false
        => ghostSnapshotCash == 0 && ghostSnapshotBorrows == 0;

// VS- | Snapshot stamp MUST be always equal to 1
invariant snapshotStampAlwaysOne() ghostSnapshotStamp == 1;

// VS- | last interest accumulator timestamp MUST NOT be in the future
invariant lastInterestAccumulatorNotInFuture(env e) 
    // Assume it is zero after constructor as it is not possible to set current timestamp as init_axiom state 
    ghostLastInterestAccumulatorUpdate <= to_mathint(e.block.timestamp) {
        preserved with (env eFunc) {
            requireValidTimeStamp(e, eFunc);
        } 
    }

// VS- | Last interest accumulator timestamp set when positive accumulated fees
invariant timestampSetWhenPositiveAccumulatedFees(env e) 
    ghostAccumulatedFees != 0 => ghostLastInterestAccumulatorUpdate != 0 {
        preserved with (env eFunc) {
            requireValidTimeStamp(e, eFunc);
        } 
    }

// VS- | Cash amount MUST NOT be less than the ERC20 assets stored in the current contract
invariant cashNotLessThanAssets() 
    ghostErc20Balances[currentContract] >= ghostCash;

// VS- | Max supply and borrow caps limitations
invariant supplyBorrowCapsLimits() 
    to_mathint(storage_supplyCap()) <= 2 * MAX_SANE_AMOUNT() || storage_supplyCap() == max_uint256
    && to_mathint(storage_borrowCap()) <= MAX_SANE_AMOUNT() || storage_borrowCap() == max_uint256;

// VS- | Hooks limitations
invariant hooksLimits() 
    ghostHookedOps < OP_MAX_VALUE();

// VS- | Total shares, total borrows, accumulated fees limitations
invariant totalSharesBorrowsFeeLimits() 
    ghostTotalShares < MAX_SANE_AMOUNT() 
    && ghostTotalBorrows < MAX_SANE_DEBT_AMOUNT()
    && ghostAccumulatedFees < MAX_SANE_AMOUNT();

// VS- | Shares cannot be transferred to the zero address
invariant validateNotUseZeroAddress() ghostUsersDataBalance[0] == 0
    // Use selectors instead of preserved block, because specification tested with different 
    //  contracts and there is no other need to put them into sceene 
    filtered { 
        f -> f.selector != 0xc1342574   // Exclude liquidate() as `violator` can be set to zero
        && f.selector != 0xaebde56b     // Exclude pullDebt() as `from` can be set to zero
    }

//
// LTV
//

// VS- | Self-collateralization is not allowed
invariant noSelfCollateralization() 
    !ghostLtvInitialized[currentContract] == false 
    && ghostBorrowLTV[currentContract] == 0 
    && ghostLiquidationLTV[currentContract] == 0;

// VS- | The borrow LTV must be lower than or equal to the liquidation LTV
invariant borrowLTVLowerOrEqualLiquidationLTV(address collateral) 
    ghostBorrowLTV[collateral] <= ghostLiquidationLTV[collateral];

// VS- | The LTV is always initialized when set
invariant initializedLTVWhenSet(address collateral) 
    ghostBorrowLTV[currentContract] != 0 || ghostLiquidationLTV[collateral] != 0 
        => ghostLtvInitialized[collateral];

// VS- | LTV with zero timestamp should not be initialized
invariant zeroTimestampInitializedSolvency(env e, address collateral) 
    ghostLtvTargetTimestamp[collateral] == 0 
        => (ghostBorrowLTV[collateral] == 0 && ghostLiquidationLTV[collateral] == 0) {
    preserved with (env eFunc) {
        requireValidTimeStamp(e, eFunc);
    } 
}

// VS- | LTV's timestamp is always less than or equal to the current timestamp
invariant LTVTimestampValid(env e, address collateral) 
    ghostLtvTargetTimestamp[collateral] == 0 || ghostLtvTargetTimestamp[collateral] >= to_mathint(e.block.timestamp) {
        preserved with (env eFunc) {
            requireValidTimeStamp(e, eFunc);
        } 
    }

// VS- | LTV's timestamp MUST be in the future only when ramping set
invariant LTVTimestampFutureRamping(env e, address collateral)
    ghostLtvTargetTimestamp[collateral] > to_mathint(e.block.timestamp) 
        => (ghostLtvRampDuration[collateral] >= ghostLtvTargetTimestamp[collateral] - to_mathint(e.block.timestamp)) {
        preserved with (env eFunc) {
            requireValidTimeStamp(e, eFunc);
        } 
    }

// VS- | Initialized LTV exists in collaterals list
invariant initializedLTVInCollateralList(address collateral) 
    ghostLtvInitialized[collateral] <=> collateralExists(collateral) {
        preserved {
            // It should not be possible to overflow uint256 list
            require(ltvListLength() < max_uint64);
        }
    }

// VS- | Zero timestamp means the LTV is cleared or not set yet
invariant zeroTimestampIndicatesLTVCleared(env e, address collateral) 
    ghostLtvTargetTimestamp[collateral] == 0
        => ghostLiquidationLTV[collateral] == 0 && ghostInitialLiquidationLTV[collateral] == 0
            && ghostLtvRampDuration[collateral] == 0 && ghostBorrowLTV[collateral] == 0 {
        preserved with (env eFunc) {
            requireValidTimeStamp(e, eFunc);
        } 
    }

// VS- | Config parameters are scaled to `1e4`
invariant configParamsScaledTo1e4(address collateral) 
    ghostBorrowLTV[collateral] <= CONFIG_SCALE() && ghostLiquidationLTV[collateral] <= CONFIG_SCALE()
    && ghostInterestFee <= CONFIG_SCALE() && ghostMaxLiquidationDiscount <= CONFIG_SCALE();
    // && ghostInitialLiquidationLTV[collateral] <= CONFIG_SCALE()

// VS- | All collateral entries in the vault storage LTV list MUST be unique
invariant uniqueLTVEntries() 
    forall mathint i. forall mathint j. ghostLTVList[i] != ghostLTVList[j];