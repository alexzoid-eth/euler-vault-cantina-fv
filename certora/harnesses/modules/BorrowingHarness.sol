// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.0;

import "../AbstractBaseHarness.sol";
import "../../../src/EVault/modules/Borrowing.sol";

contract BorrowingHarness is AbstractBaseHarness, Borrowing {
    constructor(Integrations memory integrations) Borrowing(integrations) {}

    function updateVault() internal override(AbstractBaseHarness, Cache) returns (VaultCache memory) {
        return AbstractBaseHarness.updateVault();
    }
}