function requireValidStateCVL() {
    requireInvariant vaultNotDeinitialized;
    requireInvariant uninitializedSnapshotReset;
    requireInvariant snapshotStampAlwaysOne;
    requireInvariant cashNotLessThanAssets;
    requireInvariant supplyBorrowCapsLimits;
    requireInvariant hooksLimits;
    requireInvariant accumulatedFeesLimits;
    requireInvariant validateNotUseZeroAddress;
    requireInvariant noSelfCollateralization;
    requireInvariant uniqueLTVEntries;
    requireInvariant ltvFractionScaled;
    requireInvariant configFlagsLimits;
    requireInvariant transferNotAllowedToZeroAddress;
    requireInvariant userInterestAccumulatorLeqVault;
    requireInvariant interestAccumulatorScaledBy1e27;
    requireInvariant interestRateZeroWithoutModel;
    requireInvariant interestRateMaxLimit;
    requireInvariant differentOwnerAndSpenderAllowances;
}

function requireValidStateEnvCVL(env e) {
    requireValidStateCVL();
    requireValidTimeStamp(e);
    requireInvariant lastInterestAccumulatorNotInFuture(e);
    requireInvariant timestampSetWhenPositiveAccumulatedFees(e);
}

function requireValidStateCollateralCVL(address collateral) {
    requireInvariant borrowLTVLowerOrEqualLiquidationLTV(collateral);
    requireInvariant initializedLTVWhenSet(collateral);
    requireInvariant initializedLTVInCollateralList(collateral);
    requireInvariant configParamsScaledTo1e4(collateral);
}

function requireValidStateEnvCollateralCVL(env e, address collateral) {
    requireValidStateEnvCVL(e);
    requireValidStateCollateralCVL(collateral);
    requireInvariant zeroTimestampInitializedSolvency(e, collateral);
    requireInvariant ltvTimestampValid(e, collateral);
    requireInvariant ltvTimestampFutureRamping(e, collateral);
    requireInvariant zeroTimestampIndicatesLTVCleared(e, collateral);
    requireInvariant ltvLiquidationDynamic(e, collateral);
    requireInvariant ltvRampingTimeWithinBounds(e, collateral);
}

function requireValidStateUser(address user) {
    requireValidStateCVL();
    requireInvariant userInterestAccumulatorSetWithNonZeroOwed(user);
}

// ST-01 | Vault MUST NOT be deinitialized
invariant vaultNotDeinitialized() 
    ghostInitialized == true
    filtered { f -> !HARNESS_METHODS(f) }

// ST-02 | Uninitialized snapshot MUST be reset
invariant uninitializedSnapshotReset() 
    ghostSnapshotInitialized == false => ghostSnapshotCash == 0 && ghostSnapshotBorrows == 0
    filtered { f -> !HARNESS_METHODS(f) }

// ST-03 | Snapshot stamp MUST be always equal to 1
invariant snapshotStampAlwaysOne() 
    ghostSnapshotStamp == 1
    filtered { f -> !HARNESS_METHODS(f) }

// ST-04 | Last interest accumulator timestamp set when positive accumulated fees
invariant timestampSetWhenPositiveAccumulatedFees(env e) 
    ghostAccumulatedFees != 0 => ghostLastInterestAccumulatorUpdate != 0 
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved with (env eFunc) {
            requireValidTimeStampInv(e, eFunc);
        } 
    }

// ST-05 | Last interest accumulator timestamp MUST NOT be in the future
invariant lastInterestAccumulatorNotInFuture(env e) 
    // Assume it is zero after constructor as it is not possible to set current timestamp as init_axiom state 
    ghostLastInterestAccumulatorUpdate <= to_mathint(e.block.timestamp) 
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved with (env eFunc) {
            requireValidTimeStampInv(e, eFunc);
        } 
    }

// ST-06 | Cash amount MUST NOT be less than the ERC20 assets stored in the current contract
invariant cashNotLessThanAssets() 
    ghostErc20Balances[currentContract] >= ghostCash
    filtered { f -> !HARNESS_METHODS(f) }

// ST-07 | Max supply and borrow caps limitations
invariant supplyBorrowCapsLimits() 
    to_mathint(storage_supplyCap()) <= 2 * MAX_SANE_AMOUNT() || storage_supplyCap() == max_uint256
    && to_mathint(storage_borrowCap()) <= MAX_SANE_AMOUNT() || storage_borrowCap() == max_uint256
    filtered { f -> !HARNESS_METHODS(f) }

// ST-08 | Hooks limitations
invariant hooksLimits() 
    ghostHookedOps < OP_MAX_VALUE()
    filtered { f -> !HARNESS_METHODS(f) }

// ST-09 | Accumulated fees limitations
invariant accumulatedFeesLimits() 
    ghostAccumulatedFees < MAX_SANE_AMOUNT()
    filtered { f -> !HARNESS_METHODS(f) }

// ST-10 | Shares cannot be transferred to the zero address
invariant validateNotUseZeroAddress() 
    ghostUsersDataBalance[0] == 0
    // Use selectors instead of preserved block, because specification tested with different 
    //  contracts and there is no other need to put them into scene 
    filtered { f -> 
        !HARNESS_METHODS(f)
        && f.selector != 0xc1342574   // Exclude liquidate() as `violator` can be set to zero
        && f.selector != 0xaebde56b   // Exclude pullDebt() as `from` can be set to zero
    }

// ST-11 | Self-collateralization is not allowed
invariant noSelfCollateralization() 
    !ghostLtvInitialized[currentContract] == false 
    && ghostBorrowLTV[currentContract] == 0 
    && ghostLiquidationLTV[currentContract] == 0
    filtered { f -> !HARNESS_METHODS(f) }

// ST-12 | The borrow LTV must be lower than or equal to the liquidation LTV
invariant borrowLTVLowerOrEqualLiquidationLTV(address collateral) 
    ghostBorrowLTV[collateral] <= ghostLiquidationLTV[collateral]
    filtered { f -> !HARNESS_METHODS(f) }

// ST-13 | The LTV is always initialized when set
invariant initializedLTVWhenSet(address collateral) 
    ghostBorrowLTV[currentContract] != 0 || ghostLiquidationLTV[collateral] != 0 
        => ghostLtvInitialized[collateral]
    filtered { f -> !HARNESS_METHODS(f) }

// ST-14 | LTV with zero timestamp should not be initialized
invariant zeroTimestampInitializedSolvency(env e, address collateral) 
    ghostLtvTargetTimestamp[collateral] == 0 
        => (ghostBorrowLTV[collateral] == 0 && ghostLiquidationLTV[collateral] == 0) 
    filtered { f -> !HARNESS_METHODS(f) } {
    preserved with (env eFunc) {
        requireValidTimeStampInv(e, eFunc);
    } 
}

// ST-15 | LTV's timestamp is always less than or equal to the current timestamp
invariant ltvTimestampValid(env e, address collateral) 
    ghostLtvTargetTimestamp[collateral] == 0 || ghostLtvTargetTimestamp[collateral] >= to_mathint(e.block.timestamp) 
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved with (env eFunc) {
            requireValidTimeStampInv(e, eFunc);
        } 
    }

// ST-16 | LTV's timestamp MUST be in the future only when ramping set
invariant ltvTimestampFutureRamping(env e, address collateral)
    ghostLtvTargetTimestamp[collateral] > to_mathint(e.block.timestamp) 
        => (ghostLtvRampDuration[collateral] >= ghostLtvTargetTimestamp[collateral] - to_mathint(e.block.timestamp)) 
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved with (env eFunc) {
            requireValidTimeStampInv(e, eFunc);
        } 
    }

// ST-17 | Initialized LTV exists in collaterals list
invariant initializedLTVInCollateralList(address collateral) 
    ghostLtvInitialized[collateral] <=> collateralExists(collateral) 
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved {
            // It should not be possible to overflow uint256 list
            require(ltvListLength() < max_uint64);
        }
    }

// ST-18 | Zero timestamp means the LTV is cleared or not set yet
invariant zeroTimestampIndicatesLTVCleared(env e, address collateral) 
    ghostLtvTargetTimestamp[collateral] == 0
        => ghostLiquidationLTV[collateral] == 0 && ghostInitialLiquidationLTV[collateral] == 0
            && ghostLtvRampDuration[collateral] == 0 && ghostBorrowLTV[collateral] == 0 
        filtered { f -> !HARNESS_METHODS(f) } {
        preserved with (env eFunc) {
            requireValidTimeStampInv(e, eFunc);
        } 
    }

// ST-19 | Config parameters are scaled to `1e4`
invariant configParamsScaledTo1e4(address collateral) 
    ghostBorrowLTV[collateral] <= CONFIG_SCALE() && ghostLiquidationLTV[collateral] <= CONFIG_SCALE()
    && ghostInterestFee <= CONFIG_SCALE() && ghostMaxLiquidationDiscount <= CONFIG_SCALE()
    filtered { f -> !HARNESS_METHODS(f) } 

// ST-20 | All collateral entries in the vault storage LTV list MUST be unique
invariant uniqueLTVEntries() 
    forall mathint i. forall mathint j. ghostLTVList[i] != ghostLTVList[j]
    filtered { f -> !HARNESS_METHODS(f) }

// ST-21 | The specified LTV is a fraction between 0 and 1 (scaled by 10,000)
invariant ltvFractionScaled() 
    forall address collateral. 
        ghostBorrowLTV[collateral] <= CONFIG_SCALE() && ghostLiquidationLTV[collateral] <= CONFIG_SCALE()
    filtered { f -> !HARNESS_METHODS(f) }

// ST-22 | Liquidation LTV is calculated dynamically only when ramping is in progress and always between the target liquidation LTV and the initial liquidation LTV
invariant ltvLiquidationDynamic(env e, address collateral) 
    ghostLtvRampDuration[collateral] == 0
    ? ghostLiquidationLTV[collateral] == to_mathint(getLiquidationLTV(e, collateral))
    : ghostLiquidationLTV[collateral] <= to_mathint(getLiquidationLTV(e, collateral))
        && to_mathint(getLiquidationLTV(e, collateral)) <= ghostInitialLiquidationLTV[collateral]
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved with (env eFunc) {
            requireValidTimeStampInv(e, eFunc);
            requireInvariant ltvTimestampFutureRamping(e, collateral);
            requireInvariant ltvTimestampValid(e, collateral);
        }
    }

// ST-23 | When ramping is in progress, the time remaining is always less than or equal to the ramp duration
invariant ltvRampingTimeWithinBounds(env e, address collateral) 
    ghostLtvRampDuration[collateral] != 0
        => (ghostLtvTargetTimestamp[collateral] - to_mathint(e.block.timestamp) 
            <= ghostLtvRampDuration[collateral]
            )
    filtered { f -> !HARNESS_METHODS(f) } {
        preserved with (env eFunc) {
            requireValidTimeStampInv(e, eFunc);
            requireInvariant ltvTimestampFutureRamping(e, collateral);
            requireInvariant ltvTimestampValid(e, collateral);
        } 
    }

// ST-24 | Config flags limitations
invariant configFlagsLimits()
    ghostConfigFlags < CFG_MAX_VALUE()
    filtered { f -> !HARNESS_METHODS(f) }

// ST-25 | Transfer assets to zero address not allowed
invariant transferNotAllowedToZeroAddress()
    ghostErc20Balances[0] == 0
    filtered { f -> !HARNESS_METHODS(f) }

// ST-26 | Interest rate has a maximum limit of 1,000,000 APY
invariant interestRateMaxLimit()
    ghostInterestRate <= MAX_ALLOWED_INTEREST_RATE()
    filtered { f -> !HARNESS_METHODS(f) } 

// ST-27 | User interest accumulator always less or equal vault interest accumulator
invariant userInterestAccumulatorLeqVault()
    forall address user. ghostUsersInterestAccumulator[user] <= ghostInterestAccumulator
    filtered { f -> !HARNESS_METHODS(f) }

// ST-28 | User's interest accumulator set when non-zero owed
invariant userInterestAccumulatorSetWithNonZeroOwed(address user)
    getAccountOwed(user) != 0 => ghostUsersInterestAccumulator[user] != 0
    filtered { f -> !HARNESS_METHODS(f) }

// ST-29 | Interest accumulator is scaled by 1e27
invariant interestAccumulatorScaledBy1e27() 
    ghostInterestAccumulator >= INTEREST_ACCUMULATOR_SCALE()
    && (forall address user. ghostUsersInterestAccumulator[user] == 0 
        || ghostUsersInterestAccumulator[user] >= INTEREST_ACCUMULATOR_SCALE())
    filtered { f -> !HARNESS_METHODS(f) }

// ST-30 | Interest rate zero when interest rate model contract is not set
invariant interestRateZeroWithoutModel()
    ghostInterestRateModel == 0 => ghostInterestRate == 0
    filtered { f -> !HARNESS_METHODS(f) } 

// ST-31 | Owner and spender in allowances should differ
invariant differentOwnerAndSpenderAllowances()
    forall address i. forall address j. i == j => ghostUsersETokenAllowance[i][j] == 0
    filtered { f -> !HARNESS_METHODS(f) } 


