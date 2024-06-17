// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.0;

import "../../src/EVault/shared/Base.sol";

// This exists so that Base.LTVConfig and other type declarations 
// are available in CVL and can be used across specs for different modules.
// We need to split this into a concrete contract and an Abstract contract
// so that we can refer to Base.LTVConfig as a type in shared CVL functions
// while also making function definitions sharable among harnesses via
// AbstractBase. AbstractBaseHarness includes the shared function definitions.
abstract contract AbstractBaseHarness is Base {

    constructor() {
        vaultStorage.interestAccumulator = 1e27;
        snapshot.reset();
    }

    function updateVault() internal override virtual returns (VaultCache memory vaultCache) {
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

    function LTVFullHarness(address collateral) public view returns (uint16, uint16, uint16, uint48, uint32) {
        LTVConfig memory ltv = vaultStorage.ltvLookup[collateral];
        return (
            ltv.borrowLTV.toUint16(),
            ltv.liquidationLTV.toUint16(),
            ltv.initialLiquidationLTV.toUint16(),
            ltv.targetTimestamp,
            ltv.rampDuration
        );
    }

    function isKnownNonOwnerAccountHarness(address account) public returns (bool) {
        return isKnownNonOwnerAccount(account);
    }

    function evcCompatibleAsset() public returns (bool) {
        return vaultStorage.configFlags.isSet(CFG_EVC_COMPATIBLE_ASSET);
    }

    function touchHarness() public {
        initOperation(OP_TOUCH, CHECKACCOUNT_NONE);
    }

    function getBorrowLTV(address collateral) public view returns (uint16) {
        return vaultStorage.ltvLookup[collateral].getLTV(false).toUint16();
    }

    function getLiquidationLTV(address collateral) public view returns (uint16) {
        return vaultStorage.ltvLookup[collateral].getLTV(true).toUint16();
    }

    function getAccountOwed(address account) public returns (uint256) {
        return vaultStorage.users[account].getOwed().toUint();
    }

    function isBalanceAndBalanceEnabled(address account) public returns (bool) {
        (, bool enabled) = vaultStorage.users[account].getBalanceAndBalanceForwarder();
        return enabled;
    }

    function isOperationDisabledExt(uint32 operation) public returns (bool) {
        VaultCache memory vaultCache = updateVault();
        return isOperationDisabled(vaultCache.hookedOps, operation);
    }

    function isDepositDisabled() public returns (bool) {
        return isOperationDisabledExt(OP_DEPOSIT);
    }

    function isMintDisabled() public returns (bool) {
        return isOperationDisabledExt(OP_MINT);
    }

    function isWithdrawDisabled() public returns (bool) {
        return isOperationDisabledExt(OP_WITHDRAW);
    }

    function isRedeemDisabled() public returns (bool) {
        return isOperationDisabledExt(OP_REDEEM);
    }

    function isSkimDisabled() public returns (bool) {
        return isOperationDisabledExt(OP_SKIM);
    }

    function isHookNotSet(uint32 flag) public view returns (bool) {
        return vaultStorage.hookedOps.isNotSet(flag);
    }

    function collateralExists(address collateral) public view returns (bool) {
        uint256 length = vaultStorage.ltvList.length;
        for (uint256 i; i < length; ++i) {
            if (vaultStorage.ltvList[i] == collateral) {
                return true;
            }
        }
        return false;
    }

    function ltvListLength() public view returns (uint256) {
        return vaultStorage.ltvList.length;
    }

    function storage_supplyCap() public view returns (uint256) {
        return vaultStorage.supplyCap.resolve();
    }
    function storage_borrowCap() public view returns (uint256) {
        return vaultStorage.borrowCap.resolve();
    }

    function getEVC() public view returns (address) {
        return address(evc);
    }
}