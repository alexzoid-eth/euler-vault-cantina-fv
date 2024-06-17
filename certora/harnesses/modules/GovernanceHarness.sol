// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.0;

import "../AbstractBaseHarness.sol";
import "../../../src/EVault/modules/Governance.sol";

contract GovernanceHarness is AbstractBaseHarness, Governance {
    constructor(Integrations memory integrations) Governance (integrations) {}    

    function updateVault() internal override(AbstractBaseHarness, Cache) returns (VaultCache memory) {
        return AbstractBaseHarness.updateVault();
    }

    function isSenderGovernor() public view returns (bool) {
        return governorAdmin() == EVCAuthenticateGovernor();
    }
}