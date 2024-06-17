// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.0;

import "../../../certora/harnesses/AbstractBaseHarness.sol";
import "../../../src/EVault/modules/Vault.sol";
import "../../../src/EVault/modules/Token.sol";

contract VaultHarness is AbstractBaseHarness, VaultModule, TokenModule {
    constructor(Integrations memory integrations) Base(integrations) {}

    function updateVault() internal override(AbstractBaseHarness, Cache) returns (VaultCache memory) {
        return AbstractBaseHarness.updateVault();
    }
}