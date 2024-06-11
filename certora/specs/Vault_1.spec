import "./base/Vault.spec";
import "./ValidState.spec";

// @todo VLT-83 | User's balance of assets MUST NOT increase after performing both input and 
//  output transactions within a single block
rule userBalanceNotIncreaseAfterInputOutputInSingleBlock(
        env e, method f1, method f2, uint256 amountIn, uint256 amountOut, address user
        ) 
    filtered { f1 -> INPUT_METHODS(f1), f2 -> OUTPUT_METHODS(f2) } {

    // Don't use permit's transferFrom (access to permit2 immutable variable directly)
    require(currentContract.permit2 == 0);

    // Initially user don't have any shares
    require(balanceOf(e, e.msg.sender) == 0);

    // Receiver is authenticated account
    require(user == ghostOnBehalfOfAccount);

    // Amount of assets before
    mathint balanceBefore = _Asset.balanceOf(e, e.msg.sender);

    // Input tokens
    if(f1.selector == sig:deposit(uint256,address).selector) {
        deposit(e, amountIn, user);
    } else if(f1.selector == sig:mint(uint256,address).selector) {
        mint(e, amountIn, user);
    }

    // Output tokens
    if(f2.selector == sig:withdraw(uint256,address,address).selector) {
        withdraw(e, amountOut, user, user);
    } else if(f2.selector == sig:redeem(uint256,address,address).selector) {
        redeem(e, amountOut, user, user);
    }

    // Amount of assets after
    mathint balanceAfter = _Asset.balanceOf(e, e.msg.sender);

    // User's assets MUST not grow in one block
    assert(balanceAfter <= balanceBefore);
}

// VLT- | Snapshot cash MUST set from storage cash or reset
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

// @todo VLT- | The vault's cash changes are synchronized with changes in total shares
rule cashSharesSynced(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_METHODS(f) } {

    requireInvariant cashNotLessThanAssets;

    mathint cashPrev = ghostCash;
    mathint totalSharesPrev = totalShares(e);
    
    f(e, args);

    /*
    uint256 amount; address receiver; address owner;
    require(owner != 0);
    require(receiver != currentContract); // @todo
    if(f.selector == sig:withdraw(uint256,address,address).selector) {
        withdraw(e, amount, receiver, owner);
    } else if(f.selector == sig:redeem(uint256,address,address).selector) {
        redeem(e, amount, receiver, owner);
    } else {
        f(e, args);
    }
    */

    assert(ghostCash != cashPrev => to_mathint(totalShares(e)) != totalSharesPrev);
}

// VLT- | Snapshot MUST NOT be used when it is not initialized
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

// @todo VLT- | Change accumulated fees accrued MUST set last interest accumulator timestamp
rule interestFeesAccruedSetTimestamp(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_METHODS(f) } {
    
    require(e.block.timestamp > 0);
    requireInvariant lastInterestAccumulatorNotInFuture(e);

    mathint accumulatedFeesPrev = accumulatedFees(e);

    f(e, args);
    
    assert(accumulatedFeesPrev != to_mathint(accumulatedFees(e))
        => ghostLastInterestAccumulatorUpdate == to_mathint(e.block.timestamp)
    );
}

// VLT- | Accumulated fees and interest accumulator are updated only when time has passed since the last update
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

// @todo VLT- | The vault's cash changes must be accompanied by either a transfer or a skimming of surplus assets
rule cashChangesWithTransferOrSkim(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_METHODS(f) } {

    requireInvariant cashNotLessThanAssets;

    mathint cashPrev = ghostCash;
    mathint erc20BalancePrev = ghostErc20Balances[currentContract];

    f(e, args);

    assert(ghostCash != cashPrev
        => (ghostCash > cashPrev
        // Cash increase => tokens were transferred to the current contract
        ? ghostErc20Balances[currentContract] - erc20BalancePrev == ghostCash - cashPrev
            // or tokens were skimmed from current contract's balance surplus
            || (ghostErc20Balances[currentContract] == erc20BalancePrev
                && ghostErc20Balances[currentContract] > cashPrev
                && ghostErc20Balances[currentContract] - cashPrev <= ghostCash - cashPrev)
        // Cash decrease => tokens were transferred out form the current contract
        : erc20BalancePrev - ghostErc20Balances[currentContract] == cashPrev - ghostCash
        )
    );
}

// VLT- | Transferring assets from the vault MUST decrease the available cash balance
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