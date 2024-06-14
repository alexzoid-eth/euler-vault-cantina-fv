function requireValidStateCVL() {
    requireInvariant vaultNotDeinitialized;
    requireInvariant uninitializedSnapshotReset;
    requireInvariant snapshotStampAlwaysOne;
    requireInvariant cashNotLessThanAssets;
    requireInvariant supplyBorrowCapsLimits;
    requireInvariant hooksLimits;
    requireInvariant totalSharesBorrowsFeeLimits;
    requireInvariant validateNotUseZeroAddress;
    requireInvariant noSelfCollateralization;
    requireInvariant uniqueLTVEntries;
}

function requireValidStateEnvCVL(env e) {
    requireInvariant lastInterestAccumulatorNotInFuture(e);
    requireInvariant timestampSetWhenPositiveAccumulatedFees(e);
}

function requireValidStateCollateralCVL(env e, address collateral) {
    requireInvariant borrowLTVLowerOrEqualLiquidationLTV(collateral);
    requireInvariant initializedLTVWhenSet(collateral);
    requireInvariant zeroTimestampInitializedSolvency(e, collateral);
    requireInvariant LTVTimestampValid(e, collateral);
    requireInvariant LTVTimestampFutureRamping(e, collateral);
    requireInvariant initializedLTVInCollateralList(collateral);
    requireInvariant zeroTimestampIndicatesLTVCleared(e, collateral);
    requireInvariant configParamsScaledTo1e4(collateral);
}

// Vault MUST NOT be deinitialized
invariant vaultNotDeinitialized() 
    ghostInitialized == true
    filtered { f -> !HARNESS_METHODS(f) }

// Uninitialized snapshot MUST be reset
invariant uninitializedSnapshotReset() 
    ghostSnapshotInitialized == false => ghostSnapshotCash == 0 && ghostSnapshotBorrows == 0
    filtered { f -> !HARNESS_METHODS(f) }

// Snapshot stamp MUST be always equal to 1
invariant snapshotStampAlwaysOne() 
    ghostSnapshotStamp == 1
    filtered { f -> !HARNESS_METHODS(f) }

// Last interest accumulator timestamp set when positive accumulated fees
invariant timestampSetWhenPositiveAccumulatedFees(env e) 
    ghostAccumulatedFees != 0 => ghostLastInterestAccumulatorUpdate != 0 
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved with (env eFunc) {
            requireValidTimeStamp(e, eFunc);
        } 
    }

// last interest accumulator timestamp MUST NOT be in the future
invariant lastInterestAccumulatorNotInFuture(env e) 
    // Assume it is zero after constructor as it is not possible to set current timestamp as init_axiom state 
    ghostLastInterestAccumulatorUpdate <= to_mathint(e.block.timestamp) 
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved with (env eFunc) {
            requireValidTimeStamp(e, eFunc);
        } 
    }

// Cash amount MUST NOT be less than the ERC20 assets stored in the current contract
invariant cashNotLessThanAssets() 
    ghostErc20Balances[currentContract] >= ghostCash
    filtered { f -> !HARNESS_METHODS(f) }

// Max supply and borrow caps limitations
invariant supplyBorrowCapsLimits() 
    to_mathint(storage_supplyCap()) <= 2 * MAX_SANE_AMOUNT() || storage_supplyCap() == max_uint256
    && to_mathint(storage_borrowCap()) <= MAX_SANE_AMOUNT() || storage_borrowCap() == max_uint256
    filtered { f -> !HARNESS_METHODS(f) }

// Hooks limitations
invariant hooksLimits() 
    ghostHookedOps < OP_MAX_VALUE()
    filtered { f -> !HARNESS_METHODS(f) }

// @todo (Vault) Total shares, total borrows, accumulated fees limitations
invariant totalSharesBorrowsFeeLimits() 
    ghostTotalShares < MAX_SANE_AMOUNT() 
    && ghostTotalBorrows < MAX_SANE_DEBT_AMOUNT()
    && ghostAccumulatedFees < MAX_SANE_AMOUNT()
    filtered { f -> !HARNESS_METHODS(f) }

// Shares cannot be transferred to the zero address
invariant validateNotUseZeroAddress() 
    ghostUsersDataBalance[0] == 0
    // Use selectors instead of preserved block, because specification tested with different 
    //  contracts and there is no other need to put them into scene 
    filtered { f -> 
        !HARNESS_METHODS(f)
        && f.selector != 0xc1342574   // Exclude liquidate() as `violator` can be set to zero
        && f.selector != 0xaebde56b   // Exclude pullDebt() as `from` can be set to zero
    }

// Self-collateralization is not allowed
invariant noSelfCollateralization() 
    !ghostLtvInitialized[currentContract] == false 
    && ghostBorrowLTV[currentContract] == 0 
    && ghostLiquidationLTV[currentContract] == 0
    filtered { f -> !HARNESS_METHODS(f) }

// The borrow LTV must be lower than or equal to the liquidation LTV
invariant borrowLTVLowerOrEqualLiquidationLTV(address collateral) 
    ghostBorrowLTV[collateral] <= ghostLiquidationLTV[collateral]
    filtered { f -> !HARNESS_METHODS(f) }

// The LTV is always initialized when set
invariant initializedLTVWhenSet(address collateral) 
    ghostBorrowLTV[currentContract] != 0 || ghostLiquidationLTV[collateral] != 0 
        => ghostLtvInitialized[collateral]
    filtered { f -> !HARNESS_METHODS(f) }

// LTV with zero timestamp should not be initialized
invariant zeroTimestampInitializedSolvency(env e, address collateral) 
    ghostLtvTargetTimestamp[collateral] == 0 
        => (ghostBorrowLTV[collateral] == 0 && ghostLiquidationLTV[collateral] == 0) 
    filtered { f -> !HARNESS_METHODS(f) } {
    preserved with (env eFunc) {
        requireValidTimeStamp(e, eFunc);
    } 
}

// LTV's timestamp is always less than or equal to the current timestamp
invariant LTVTimestampValid(env e, address collateral) 
    ghostLtvTargetTimestamp[collateral] == 0 || ghostLtvTargetTimestamp[collateral] >= to_mathint(e.block.timestamp) 
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved with (env eFunc) {
            requireValidTimeStamp(e, eFunc);
        } 
    }

// LTV's timestamp MUST be in the future only when ramping set
invariant LTVTimestampFutureRamping(env e, address collateral)
    ghostLtvTargetTimestamp[collateral] > to_mathint(e.block.timestamp) 
        => (ghostLtvRampDuration[collateral] >= ghostLtvTargetTimestamp[collateral] - to_mathint(e.block.timestamp)) 
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved with (env eFunc) {
            requireValidTimeStamp(e, eFunc);
        } 
    }

// Initialized LTV exists in collaterals list
invariant initializedLTVInCollateralList(address collateral) 
    ghostLtvInitialized[collateral] <=> collateralExists(collateral) 
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved {
            // It should not be possible to overflow uint256 list
            require(ltvListLength() < max_uint64);
        }
    }

// Zero timestamp means the LTV is cleared or not set yet
invariant zeroTimestampIndicatesLTVCleared(env e, address collateral) 
    ghostLtvTargetTimestamp[collateral] == 0
        => ghostLiquidationLTV[collateral] == 0 && ghostInitialLiquidationLTV[collateral] == 0
            && ghostLtvRampDuration[collateral] == 0 && ghostBorrowLTV[collateral] == 0 
        filtered { f -> !HARNESS_METHODS(f) } {
        preserved with (env eFunc) {
            requireValidTimeStamp(e, eFunc);
        } 
    }

// Config parameters are scaled to `1e4`
invariant configParamsScaledTo1e4(address collateral) 
    ghostBorrowLTV[collateral] <= CONFIG_SCALE() && ghostLiquidationLTV[collateral] <= CONFIG_SCALE()
    && ghostInterestFee <= CONFIG_SCALE() && ghostMaxLiquidationDiscount <= CONFIG_SCALE()
    // && ghostInitialLiquidationLTV[collateral] <= CONFIG_SCALE()
    filtered { f -> !HARNESS_METHODS(f) }

// All collateral entries in the vault storage LTV list MUST be unique
invariant uniqueLTVEntries() 
    forall mathint i. forall mathint j. ghostLTVList[i] != ghostLTVList[j]
    filtered { f -> !HARNESS_METHODS(f) }

// @todo The specified LTV is a fraction between 0 and 1 (scaled by 10,000)
invariant ltvFractionScaled(env e, address collateral) 
    to_mathint(getBorrowLTV(e, collateral)) <= CONFIG_SCALE()
    && to_mathint(getLiquidationLTV(e, collateral)) <= CONFIG_SCALE()
    filtered { f -> !HARNESS_METHODS(f) }

// @todo Liquidation LTV is calculated dynamically only when ramping is in progress and always 
//  between the target liquidation LTV and the initial liquidation LTV
invariant LTVLiquidationDynamic(env e, address collateral) ghostLtvRampDuration[collateral] > 0
    ? ghostLiquidationLTV[collateral] == to_mathint(getLiquidationLTV(e, collateral))
    : ghostLiquidationLTV[collateral] <= to_mathint(getLiquidationLTV(e, collateral))
        && to_mathint(getLiquidationLTV(e, collateral)) <= ghostInitialLiquidationLTV[collateral]
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved with (env eFunc) {
            requireValidTimeStamp(e, eFunc);
            requireInvariant LTVTimestampFutureRamping(e, collateral);
            requireInvariant LTVTimestampValid(e, collateral);
        }
    }

// @todo When ramping is in progress, the time remaining is always less than or equal to 
//  the ramp duration
invariant LTVRampingTimeWithinBounds(env e, address collateral) 
    to_mathint(e.block.timestamp) < ghostLtvTargetTimestamp[collateral]
        => (ghostLtvTargetTimestamp[collateral] - to_mathint(e.block.timestamp) 
            < ghostLtvRampDuration[collateral]
            )
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved with (env eFunc) {
            requireValidTimeStamp(e, eFunc);
        } 
    }
