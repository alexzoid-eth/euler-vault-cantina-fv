// SPDX-License-Identifier: GPL-2.0-or-later

pragma solidity ^0.8.0;
import "../../../src/interfaces/IPriceOracle.sol";
import {ERC20} from "../../../lib/ethereum-vault-connector/lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";
import "../AbstractBaseHarness.sol";
import "../../../src/EVault/modules/Liquidation.sol";

contract LiquidationHarness is AbstractBaseHarness, Liquidation {

    constructor(Integrations memory integrations) Liquidation(integrations) {}

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

    function calculateLiquidityExternal(
        address account
    ) public view returns (uint256 collateralValue, uint256 liabilityValue) {
        return calculateLiquidity(loadVault(), account, getCollaterals(account), true);
    }

    function calculateLiquidationExt(
        VaultCache memory vaultCache,
        address liquidator,
        address violator,
        address collateral,
        uint256 desiredRepay
    ) external view returns (LiquidationCache memory liqCache) {
        return calculateLiquidation(vaultCache, liquidator, violator, collateral, desiredRepay);
    }

    function isRecognizedCollateralExt(address collateral) external view virtual returns (bool) {
        return isRecognizedCollateral(collateral);
    }

    function getLiquidator() external returns (address liquidator) {
        (, liquidator) = initOperation(OP_LIQUIDATE, CHECKACCOUNT_CALLER);
    }

    function getCurrentOwedExt(VaultCache memory vaultCache, address violator) external view returns (Assets) {
        return getCurrentOwed(vaultCache, violator).toAssetsUp();
    }

    function getCollateralValueExt(VaultCache memory vaultCache, address account, address collateral, bool liquidation)
        external
        view
        returns (uint256 value) {
            return getCollateralValue(vaultCache, account, collateral, liquidation);
    }

}