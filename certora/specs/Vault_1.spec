import "methods/vault_methods.spec";
import "base/base.spec";
import "base/vault.spec";

methods {
    function _.requireVaultStatusCheck() external => CONSTANT;
    function _.getCurrentOnBehalfOfAccount(address controllerToCheck) external => CONSTANT;
    function _.balanceTrackerHook(address account, uint256 newAccountBalance, bool forfeitRecentReward) external => CONSTANT;
}

rule testAsset() {
    assert(asset() == _Asset);
}

// VLT-83 | User's balance of assets MUST NOT increase after performing both input and output transactions within a single block
rule userBalanceNotIncreaseInSingleBlock(env e, method f1, method f2, calldataarg args1, calldataarg args2) 
    filtered { f1 -> INPUT_METHODS(f1), f2 -> OUTPUT_METHODS(f2) } {

    // Initially user don't have any shares
    require(balanceOf(e, e.msg.sender) == 0);

    mathint balanceBefore = _Asset.balanceOf(e, e.msg.sender);

    // Input tokens
    f1(e, args1);

    // Output tokens
    f2(e, args2);
 
    mathint balanceAfter = _Asset.balanceOf(e, e.msg.sender);

    assert(balanceAfter <= balanceBefore);
}

