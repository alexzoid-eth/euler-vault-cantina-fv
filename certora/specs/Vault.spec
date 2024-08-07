import "./base/methods/VaultMethods.spec";
import "./base/Base.spec";
import "./common/State.spec";
import "./common/Funcs.spec";

use builtin rule sanity;
use builtin rule msgValueInLoopRule;

// VLT-01 | Accumulated fees must always be less than or equal to total shares
invariant accumulatedFeesLeqShares(address user) 
    ghostAccumulatedFees <= ghostTotalShares
    filtered { f -> !HARNESS_METHODS(f) } {
        // User's balance MUST not be greater than total shares (take scenario with only one user)
        preserved withdraw(uint256 amount, address receiver, address owner) with (env e) {
            requireInvariant userBalanceEqualTotalShares(owner);
        }
        preserved redeem(uint256 amount, address receiver, address owner) with (env e) {
            requireInvariant userBalanceEqualTotalShares(owner);
        }
    }

// VLT-02 | User balance plus accumulated fees must always be equal to the total shares (with only 1 user)
function userBalanceEqualTotalSharesReqCVL(address user) {
    // Balance of any other addresses are zero
    require(forall address u. u != user => ghostUsersDataBalance[u] == 0);
    // User not zero
    require(user != 0);
}

invariant userBalanceEqualTotalShares(address user) 
    ghostUsersDataBalance[user] + ghostAccumulatedFees == ghostTotalShares 
    filtered { f -> !HARNESS_METHODS(f) } {
    preserved {
        userBalanceEqualTotalSharesReqCVL(user);
    }
    preserved deposit(uint256 amount, address receiver) with (env e) {
        require(receiver == user);
        userBalanceEqualTotalSharesReqCVL(user);
    }
    preserved mint(uint256 amount, address receiver) with (env e) {
        require(receiver == user);
        userBalanceEqualTotalSharesReqCVL(user);
    }
    preserved skim(uint256 amount, address receiver) with (env e) {
        require(receiver == user);
        userBalanceEqualTotalSharesReqCVL(user);
    }
    preserved transfer(address to, uint256 amount) with (env e) {
        require(to == user);
        userBalanceEqualTotalSharesReqCVL(user);
    }
    preserved transferFromMax(address from, address to) with (env e) {
        require(to == user);
        userBalanceEqualTotalSharesReqCVL(user);
    }
    preserved transferFrom(address from, address to, uint256 amount) with (env e) {
        require(to == user);
        userBalanceEqualTotalSharesReqCVL(user);
    }
}

// VLT-03 | Sum of three users' balance must always be equal to the total shares (with only 3 users)
function sumOfUsersBalanceEqualTotalSharesReqCVL(address user1, address user2, address user3) {
    // Balance of any other addresses are zero
    require(forall address u. u != user1 && u != user2 && u != user3 => ghostUsersDataBalance[u] == 0);
    // All users are different and not zero
    require(user1 != user2 && user1 != user3 && user2 != user3);
    require(user1 != 0 && user2 != 0 && user3 != 0);
}

invariant sumOfUsersBalanceEqualTotalShares(address user1, address user2, address user3) 
    ghostUsersDataBalance[user1] + ghostUsersDataBalance[user2] + ghostUsersDataBalance[user3] == ghostTotalShares 
    filtered { f -> !HARNESS_METHODS(f) } {
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

// VLT-04 | The vault's cash changes must be accompanied by assets transfer (when no surplus assets available)
rule cashChangesWithTransfer(env e, method f, calldataarg args)
    filtered { f -> !HARNESS_METHODS(f) } {
    
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

    // No surplus assets were available
    assert(erc20BalancePrev == cashPrev 
        // Cash was changed
        && ghostCash != cashPrev => (ghostCash > cashPrev
        // Cash increase => tokens were transferred to the current contract
        ? ghostErc20Balances[currentContract] - erc20BalancePrev == ghostCash - cashPrev
        // Cash decrease => tokens were transferred out form the current contract
        : erc20BalancePrev - ghostErc20Balances[currentContract] == cashPrev - ghostCash
        )
    );
}

// VLT-05 | Changes in the cash balance must correspond to changes in user's shares
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

// VLT-06 | Snapshot is disabled if both caps are disabled (at low-level set to 0, but resolved to max_uint256)
invariant snapshotDisabledWithBothCapsDisabled() 
    ghostSupplyCap == 0 && ghostBorrowCap == 0 => ghostSnapshotInitialized == false
    filtered { f -> !HARNESS_METHODS(f) }

// VLT-07 | View functions don't update the state
use rule viewFunctionsDontUpdateState;

// VLT-08 | State change functions are protected against reentrancy
use rule stateChangeFunctionsReentrancyProtected;

// VLT-09 | Anyone can execute view functions
use rule anyoneCanExecuteViewFunctions;

// VLT-10 | Specific view functions are protected against reentrancy
use rule specificViewFunctionsProtectedAgainstReentrancy;

// VLT-11 | Specific functions can modify state
use rule specificFunctionsModifyState;

// VLT-12 | Possibility of modifying state
use rule modifyStatePossibility;

// VLT-13 | Hook execution allowance
use rule hookExecutionAllowance;

// VLT-14 | Hook execution possibility
use rule hookExecutionPossibility;

// VLT-15 | Hook execution restriction
use rule hookExecutionRestriction;