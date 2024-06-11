import "./base/Base.spec";

function requireValidStateCVL() {
}

// VS- | Vault MUST NOT be deinitialized
invariant vaultNotDeinitialized() ghostInitialized == true;

// VS- | Uninitialized snapshot MUST be reset
invariant uninitializedSnapshotReset() 
    ghostSnapshotInitialized == false
        => ghostSnapshotCash == 0 && ghostSnapshotBorrows == 0;

// ST- | Snapshot is disabled if both caps are disabled (at low-level set to 0, but resolved to max_uint256)
invariant snapshotDisabledWithBothCapsDisabled() 
    ghostSupplyCap == 0 && ghostBorrowCap == 0
        => ghostSnapshotInitialized == false;

// VS- | Snapshot stamp MUST be always equal to 1
invariant snapshotStampAlwaysOne() ghostSnapshotStamp == 1;

// VS- | last interest accumulator timestamp MUST NOT be in the future
invariant lastInterestAccumulatorNotInFuture(env e) 
    // Assume it is zero after constructor as it is not possible to set current timestamp as init_axiom state 
    ghostLastInterestAccumulatorUpdate == 0 
    || ghostLastInterestAccumulatorUpdate <= to_mathint(e.block.timestamp) {
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
invariant cashNotLessThanAssets() ghostErc20Balances[currentContract] >= ghostCash;



///////////////////////////////////////////////////////////////////////////////////////

// VS- | Shares cannot be transferred to the zero address
invariant validateFeeReceiverAddress() getBalance(0) == 0;

// VS- | Self-collateralization is not allowed
invariant noSelfCollateralization() ghostLtvInitialized[currentContract] == false 
    && ghostBorrowLTV[currentContract] == 0 && ghostLiquidationLTV[currentContract] == 0;

// VS- | The borrow LTV must be lower than or equal to the liquidation LTV
invariant borrowLTVLowerOrEqualLiquidationLTV(address collateral) 
    ghostBorrowLTV[collateral] <= ghostLiquidationLTV[collateral];

// VS- | The LTV is always initialized when set
invariant initializedLTVWhenSet(address collateral) 
    ghostBorrowLTV[currentContract] != 0 || ghostLiquidationLTV[collateral] != 0 
        => ghostLtvInitialized[collateral];

// VS- | LTV with zero timestamp should not be initialized and vice versa
invariant zeroTimestampInitializedSolvency(address collateral) 
    ghostLtvTargetTimestamp[collateral] == 0 
        <=> ghostBorrowLTV[currentContract] == 0 && ghostLiquidationLTV[currentContract] == 0;

// VS- | LTV's timestamp is always less than or equal to the current timestamp
invariant LTVTimestampValid(env e, address collateral) ghostLtvTargetTimestamp[collateral] == 0 
    || ghostLtvTargetTimestamp[collateral] >= to_mathint(e.block.timestamp) {
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
invariant zeroTimestampIndicatesLTVCleared(env e, address collateral) ghostLtvTargetTimestamp[collateral] == 0
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

//
// ltvList
//

// VS- | All collateral entries in the vault storage LTV list MUST be unique
invariant uniqueLTVEntries() forall mathint i. forall mathint j. ghostLTVList[i] != ghostLTVList[j];