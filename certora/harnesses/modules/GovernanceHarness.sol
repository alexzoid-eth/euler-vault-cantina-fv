// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.0;
import {ERC20} from "../../../lib/ethereum-vault-connector/lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";
import "../AbstractBaseHarness.sol";
import "../../../src/EVault/modules/Governance.sol";

contract GovernanceHarness is Governance, AbstractBaseHarness {
    constructor(Integrations memory integrations) Governance (integrations) {}    

    function updateVault() internal override returns (VaultCache memory vaultCache) {
        // initVaultCache is difficult to summarize because we can't
        // reason about the pass-by-value VaultCache at the start and
        // end of the call as separate values. So this harness
        // gives us a way to keep the loadVault summary when updateVault
        // is called
        vaultCache = loadVault();
        if(block.timestamp - vaultCache.lastInterestAccumulatorUpdate > 0) {
            vaultStorage.lastInterestAccumulatorUpdate = vaultCache.lastInterestAccumulatorUpdate;
            vaultStorage.accumulatedFees = vaultCache.accumulatedFees;

            vaultStorage.totalShares = vaultCache.totalShares;
            vaultStorage.totalBorrows = vaultCache.totalBorrows;

            vaultStorage.interestAccumulator = vaultCache.interestAccumulator;
        }
        return vaultCache;
    }

    function isSenderGovernor() public view returns (bool) {
        return governorAdmin() == EVCAuthenticateGovernor();
    }

    function accumulatedFees() public returns (uint256) {        
        VaultCache memory vaultCache = updateVault();
        return vaultCache.accumulatedFees.toUint();
    }

    function getLTVConfig(address collateral) external view returns (LTVConfig memory) {
        return vaultStorage.ltvLookup[collateral];
    }

    function getBalanceAndForwarderExt(address account) public returns (Shares, bool) {
        return vaultStorage.users[account].getBalanceAndBalanceForwarder();
    }
}