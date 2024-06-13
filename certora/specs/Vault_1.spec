import "./base/Vault.spec";
import "./Common.spec";

// VLT- | Snapshot is disabled if both caps are disabled (at low-level set to 0, but resolved to max_uint256)
invariant snapshotDisabledWithBothCapsDisabled() 
    ghostSupplyCap == 0 && ghostBorrowCap == 0 => ghostSnapshotInitialized == false;

// @todo VLT-83 | User's balance of assets MUST NOT increase after performing both input and 
//  output transactions within a single block
rule userBalanceNotIncreaseAfterInputOutputInSingleBlock(
        env e, method f1, method f2, uint256 amountIn, uint256 amountOut, address user
        ) 
    filtered { f1 -> INPUT_METHODS(f1), f2 -> OUTPUT_METHODS(f2) } {

    requireInvariant cashNotLessThanAssets;

    // Receiver is authenticated account
    require(user == ghostOnBehalfOfAccount);

    // Amount of assets before
    mathint balanceBefore = _Asset.balanceOf(e, user);

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
    mathint balanceAfter = _Asset.balanceOf(e, user);

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

// VLT- | Change accumulated fees accrued MUST set last interest accumulator timestamp
rule interestFeesAccruedSetTimestamp(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_METHODS(f) } {
    
    requireInvariant lastInterestAccumulatorNotInFuture(e);

    mathint accumulatedFeesPrev = ghostAccumulatedFees;

    f(e, args);
    
    assert(accumulatedFeesPrev != ghostAccumulatedFees
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

// VLT- | The vault's cash changes must be accompanied by assets transfer (when no surplus assets available)
rule cashChangesWithTransfer(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_METHODS(f) } {
    
    // No surplus assets available
    require(ghostErc20Balances[currentContract] == ghostCash);

    mathint cashPrev = ghostCash;
    mathint erc20BalancePrev = ghostErc20Balances[currentContract];

    uint256 amountIn; uint256 amountOut; address user;
    // Do not allow creating of surplus assets in the current contract
    require(user != currentContract);
    if(f.selector == sig:withdraw(uint256,address,address).selector) {
        withdraw(e, amountOut, user, user);
    } else if(f.selector == sig:redeem(uint256,address,address).selector) {
        redeem(e, amountOut, user, user);
    } else {
        f(e, args);
    }

    assert(ghostCash != cashPrev => (ghostCash > cashPrev
        // Cash increase => tokens were transferred to the current contract
        ? ghostErc20Balances[currentContract] - erc20BalancePrev == ghostCash - cashPrev
        // Cash decrease => tokens were transferred out form the current contract
        : erc20BalancePrev - ghostErc20Balances[currentContract] == cashPrev - ghostCash
        )
    );
}

// VLT- | The vault's cash changes without assets transfer only when surplus assets available
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

// VLT- | Changes in the cash balance must correspond to changes in the total shares
rule cashChangesAffectTotalShares(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_METHODS(f) } {

    mathint cashPrev = ghostCash;
    mathint totalSharesPrev = ghostTotalShares;

    f(e, args);

    assert(cashPrev != ghostCash => totalSharesPrev != ghostTotalShares);
}

// VLT- | Changes in the cash balance must correspond to changes in user's shares
rule cashChangesAffectUserShares(env e, method f, calldataarg args, address user) 
    filtered { f -> !HARNESS_METHODS(f) } {

    mathint cashPrev = ghostCash;
    mathint balancePrev = to_mathint(balanceOf(e, user)); 

    uint256 amountIn; uint256 amountOut;
    if(f.selector == sig:deposit(uint256,address).selector) {
        deposit(e, amountIn, user);
    } else if(f.selector == sig:mint(uint256,address).selector) {
        mint(e, amountIn, user);
    } else if(f.selector == sig:withdraw(uint256,address,address).selector) {
        withdraw(e, amountOut, user, user);
    } else if(f.selector == sig:redeem(uint256,address,address).selector) {
        redeem(e, amountOut, user, user);
    } else if(f.selector == sig:skim(uint256,address).selector) {
        skim(e, amountIn, user);
    } else {
        f(e, args);
    }

    assert(cashPrev != ghostCash => (
        ghostCash > cashPrev
        ? to_mathint(balanceOf(e, user)) > balancePrev
        : to_mathint(balanceOf(e, user)) < balancePrev
    ));
}

// [1] VLT- | Sum of three users' balance must always be equal to the total shares

function sumOfUsersBalanceEqualTotalSharesReqCVL(address user1, address user2, address user3) {
    // Balance of any other addresses are zero
    require(forall address u. u != user1 && u != user2 && u != user3 => ghostUsersDataBalance[u] == 0);
    // All users are different and not zero
    require(user1 != user2 && user1 != user3 && user2 != user3);
    require(user1 != 0 && user2 != 0 && user3 != 0);
}

invariant sumOfUsersBalanceEqualTotalShares(address user1, address user2, address user3) 
    ghostUsersDataBalance[user1] + ghostUsersDataBalance[user2] + ghostUsersDataBalance[user3] 
        == ghostTotalShares {
    preserved {
        sumOfUsersBalanceEqualTotalSharesReqCVL(user1, user2, user3);
    }
    preserved deposit(uint256 amount, address receiver) with (env e) {
        require(receiver == user1 || receiver == user2 || receiver == user3);
        sumOfUsersBalanceEqualTotalSharesReqCVL(user1, user2, user3);
    }
    preserved mint(uint256 amount, address receiver) with (env e) {
        require(receiver == user1 || receiver == user2 || receiver == user3);
        sumOfUsersBalanceEqualTotalSharesReqCVL(user1, user2, user3);
    }
    preserved skim(uint256 amount, address receiver) with (env e) {
        require(receiver == user1 || receiver == user2 || receiver == user3);
        sumOfUsersBalanceEqualTotalSharesReqCVL(user1, user2, user3);
    }
    preserved transfer(address to, uint256 amount) with (env e) {
        require(to == user1 || to == user2 || to == user3);
        sumOfUsersBalanceEqualTotalSharesReqCVL(user1, user2, user3);
    }
    preserved transferFromMax(address from, address to) with (env e) {
        require(to == user1 || to == user2 || to == user3);
        sumOfUsersBalanceEqualTotalSharesReqCVL(user1, user2, user3);
    }
    preserved transferFrom(address from, address to, uint256 amount) with (env e) {
        require(to == user1 || to == user2 || to == user3);
        sumOfUsersBalanceEqualTotalSharesReqCVL(user1, user2, user3);
    }
}

// VLT- | Accumulated fees must not decrease unless they are being reset to zero
rule accumulatedFeesNonDecreasing(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_METHODS(f) } {

    mathint accumulatedFeesPrev = ghostAccumulatedFees;

    f(e, args);
    
    assert(ghostAccumulatedFees == 0 || ghostAccumulatedFees >= accumulatedFeesPrev);
}