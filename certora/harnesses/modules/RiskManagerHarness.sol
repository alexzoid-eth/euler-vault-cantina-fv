// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.0;

import "../AbstractBaseHarness.sol";
import "../../../src/EVault/modules/RiskManager.sol";

contract RiskManagerHarness is AbstractBaseHarness, RiskManager {
    constructor(Integrations memory integrations) RiskManager(integrations) {}

    function updateVault() internal override(AbstractBaseHarness, Cache) returns (VaultCache memory) {
        return AbstractBaseHarness.updateVault();
    }
}