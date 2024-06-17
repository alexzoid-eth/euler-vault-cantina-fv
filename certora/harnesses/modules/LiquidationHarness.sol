// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.0;

import "../AbstractBaseHarness.sol";
import "../../../src/EVault/modules/Liquidation.sol";

contract LiquidationHarness is AbstractBaseHarness, Liquidation {

    constructor(Integrations memory integrations) Liquidation(integrations) {}

    function updateVault() internal override(AbstractBaseHarness, Cache) returns (VaultCache memory) {
        return AbstractBaseHarness.updateVault();
    }

    function calculateLiquidityExt(
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