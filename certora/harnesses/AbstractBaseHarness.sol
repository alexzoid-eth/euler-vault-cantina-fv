// SPDX-License-Identifier: GPL-2.0-or-later

pragma solidity ^0.8.0;

import {IEVC} from "ethereum-vault-connector/interfaces/IEthereumVaultConnector.sol";
import "../../src/EVault/shared/Base.sol";
import "../../src/EVault/modules/Initialize.sol";

// This exists so that Base.LTVConfig and other type declarations 
// are available in CVL and can be used across specs for different modules.
// We need to split this into a concrete contract and an Abstract contract
// so that we can refer to Base.LTVConfig as a type in shared CVL functions
// while also making function definitions sharable among harnesses via
// AbstractBase. AbstractBaseHarness includes the shared function definitions.
abstract contract AbstractBaseHarness is InitializeModule  {

    constructor() {
        initialize(msg.sender);
    }

    function borrowsToAssetsUp(uint256 amount) public returns (uint256) {
        return TypesLib.toAssets(OwedLib.toAssetsUpUint(amount)).toUint();
    }

    function vaultCacheOracleConfigured() external returns (bool) {
        return address(loadVault().oracle) != address(0);
    }

    function isAccountStatusCheckDeferredExt(address account) external view returns (bool) {
        return isAccountStatusCheckDeferred(account);
    }
    
    function getBalance(address account) public returns (uint256) {
        (Shares shares, ) = vaultStorage.users[account].getBalanceAndBalanceForwarder();
        return shares.toUint();
    }

    function isBalanceAndBalanceEnabled(address account) public returns (bool) {
        (, bool enabled) = vaultStorage.users[account].getBalanceAndBalanceForwarder();
        return enabled;
    }


    //--------------------------------------------------------------------------
    // Controllers
    //--------------------------------------------------------------------------
    function vaultIsOnlyController(address account) external view returns (bool) {
        address[] memory controllers = IEVC(evc).getControllers(account);
        return controllers.length == 1 && controllers[0] == address(this);
    }

    function vaultIsController(address account) external view returns (bool) {
        return IEVC(evc).isControllerEnabled(account, address(this));
    }

    //--------------------------------------------------------------------------
    // Collaterals
    //--------------------------------------------------------------------------
    function getCollateralsExt(address account) public view returns (address[] memory) {
        return getCollaterals(account);
    }

    function isCollateralEnabledExt(address account, address market) external view returns (bool) {
        return isCollateralEnabled(account, market);
    }


    //--------------------------------------------------------------------------
    // Operation disable checks
    //--------------------------------------------------------------------------
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


    //--------------------------------------------------------------------------
    // Storage viewers
    //--------------------------------------------------------------------------
    function reentrancyLocked() public view returns (bool) {
        return vaultStorage.reentrancyLocked;
    }

    function hookTarget() public view returns (address) {
        return vaultStorage.hookTarget;
    }

    function totalShares() public returns (uint256) {
        VaultCache memory vaultCache = updateVault();
        return vaultCache.totalShares.toUint();
    }

    //--------------------------------------------------------------------------
    // Hooks set checks
    //--------------------------------------------------------------------------
    function isHookNotSetConvertFees() public view returns (bool) {
        return vaultStorage.hookedOps.isNotSet(OP_CONVERT_FEES);
    }

    //--------------------------------------------------------------------------
    // Utils
    //--------------------------------------------------------------------------
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
}