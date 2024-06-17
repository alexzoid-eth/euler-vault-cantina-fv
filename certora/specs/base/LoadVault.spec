// parameter is meant to be block.timestamp
persistent ghost newInterestBorrows(uint256) returns uint256;

function loadVaultAssumeNoUpdateCVL(env e) returns BaseHarness.VaultCache {
    BaseHarness.VaultCache vaultCache;
    uint48 lastUpdate = require_uint48(ghostLastInterestAccumulatorUpdate);
    BaseHarness.Owed oldTotalBorrows = require_uint144(ghostTotalBorrows); 
    BaseHarness.Shares oldTotalShares = require_uint112(ghostTotalShares);
    require vaultCache.cash == require_uint112(ghostCash);
    uint48 timestamp48 = require_uint48(e.block.timestamp);
    bool updated = timestamp48 != lastUpdate;
    require !updated;
    require vaultCache.lastInterestAccumulatorUpdate == lastUpdate;
    require vaultCache.totalBorrows == oldTotalBorrows;
    require vaultCache.totalShares == oldTotalShares;
    require vaultCache.accumulatedFees == require_uint112(ghostAccumulatedFees);
    require vaultCache.interestAccumulator == require_uint256(ghostInterestAccumulator);
    // unmodified values
    require vaultCache.supplyCap == storage_supplyCap();
    require vaultCache.borrowCap == storage_borrowCap();
    require vaultCache.hookedOps == require_uint32(ghostHookedOps);
    require vaultCache.configFlags == require_uint32(ghostConfigFlags);
    require vaultCache.snapshotInitialized == ghostSnapshotInitialized;

    require vaultCache.asset == _Asset;
    require vaultCache.oracle == ghostOracleAddress;
    require vaultCache.unitOfAccount == ghostUnitOfAccount;

    return vaultCache;
}
