import "./base/Vault.spec";

// VLT-83 | User's balance of assets MUST NOT increase after performing both input and output transactions within a single block
rule userBalanceNotIncreaseAfterInputOutputInSingleBlock(env e, method f1, method f2, uint256 amountIn, uint256 amountOut, address user) 
    filtered { f1 -> INPUT_METHODS(f1), f2 -> OUTPUT_METHODS(f2) } {

    // Don't use permit's transferFrom (access to permit2 immutable variable directly)
    require(currentContract.permit2 == 0);

    // Initially user don't have any shares
    require(balanceOf(e, e.msg.sender) == 0);

    // Receiver is authenticated account
    require(user == ghostOnBehalfOfAccount);

    // Amount of assets before
    mathint balanceBefore = _ERC20A.balanceOf(e, e.msg.sender);

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
    mathint balanceAfter = _ERC20A.balanceOf(e, e.msg.sender);

    // User's assets MUST not grow in one block
    assert(balanceAfter <= balanceBefore);
}

