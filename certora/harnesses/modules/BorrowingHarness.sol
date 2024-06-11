pragma solidity ^0.8.0;
import "../../../src/EVault/modules/Borrowing.sol";
import "../../../src/EVault/shared/types/UserStorage.sol";
import "../../../src/EVault/shared/types/Types.sol";
import {ERC20} from "../../../lib/ethereum-vault-connector/lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";
import "../AbstractBaseHarness.sol";

uint256 constant SHARES_MASK = 0x000000000000000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFFFFFF;

contract BorrowingHarness is AbstractBaseHarness, Borrowing {
    constructor(Integrations memory integrations) Borrowing(integrations) {}

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

    function initOperationExternal(uint32 operation, address accountToCheck)
        public 
        returns (VaultCache memory vaultCache, address account)
    {
        return initOperation(operation, accountToCheck);
    }

    function getTotalBalance() external view returns (Shares) {
        return vaultStorage.totalShares;
    }

    function toAssetsExt(uint256 amount) external pure returns (uint256){
        return TypesLib.toAssets(amount).toUint();
    }

    function unpackBalanceExt(PackedUserSlot data) external view returns (Shares) {
        return Shares.wrap(uint112(PackedUserSlot.unwrap(data) & SHARES_MASK));
    }

    function getUserInterestAccExt(address account) external view returns (uint256) {
        return vaultStorage.users[account].interestAccumulator;
    }

    function getVaultInterestAccExt() external returns (uint256) {
        VaultCache memory vaultCache = updateVault();
        return vaultCache.interestAccumulator;
    }

     function getUnderlyingAssetExt() external returns (IERC20) {
        VaultCache memory vaultCache = updateVault();
        return vaultCache.asset;
    }

}