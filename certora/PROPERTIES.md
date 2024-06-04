# Properties

**Category**: List of properties following the categorization by [Certora](https://github.com/Certora/Tutorials/blob/master/06.Lesson_ThinkingProperties/Categorizing_Properties.pdf):

- High Level
- Valid States
- State Transitions
- Variable Transitions
- Unit Tests

**Tag**: Represents the general area or feature the property relates to

**Entries**: Lists the specific functions that are involved in the property

**Mutation**: Path to the mutated file used to prove the property

**Status**: Each property is assigned a verification status:

- 📝 Todo
- ✅ Not Violated
- ⭕ Timeout
- ❌ Violated

Additionally, each property is assigned a mutation status:

- ❎ Mutation Caught
- ❗ Mutation Skipped

## Governance

| Property | Description | Category | Tag | Entries | Mutation | Status |
| --- | --- | --- | --- | --- | --- | --- |
| GOV-01 | Only the governor can invoke methods that modify the configuration of the vault |  | Governor | `governorOnly` | [Governance_Governor/1.sol](mutations/Governance_Governor/1.sol) | ✅❎ |
| GOV-73 | Non-governor methods MUST be accessible to any callers |  | Governor | `governorOnly` | [Governance_Governor/2.sol](mutations/Governance_Governor/2.sol) | ✅❎ |
| GOV-02 | Only one governor can exist at one time |  | Governor |  | [Governance_Governor/3.sol](mutations/Governance_Governor/3.sol) | ✅❎ |
| GOV-03 | When the sender is `EVC`, the governor's address is extracted from the operation's current account on behalf |  | EVCClient | `governorOnly` |  |  |
| GOV-04 | Governor's functions cannot be executed from `EVC` when the authenticated account is a governor's sub-account |  | EVCClient | `governorOnly` |  |  |
| GOV-05 | Governor's functions cannot be executed from `EVC` when an operator is authenticated |  | EVCClient | `governorOnly` |  |  |
| GOV-06 | Governor's functions cannot be executed from `EVC` when control collateral is in progress |  | EVCClient | `governorOnly` |  |  |
| GOV-07 | When the sender is not `EVC`, the governor's address is set as `msg.sender` |  | EVCClient | `governorOnly` |  |  |
| GOV-08 | Governor's functions don't process any additional check in `EVC` when the sender is not `EVC` |  | EVCClient | `governorOnly` |  |  |
| GOV-74 | Specific functions can modify state |  | Base |  | [Governance_Base/1.sol](mutations/Governance_Base/1.sol) | ✅ |
| GOV-09 | Specific functions require a vault status check |  | Base |  | [Governance_Base/2.sol](mutations/Governance_Base/2.sol) | ✅ |
| GOV-10 | Specific functions execute a hook |  | Base |  |  |  |
| GOV-11 | Vault's storage can be updated from cache when specific functions are executed |  | Base |  |  |  |
| GOV-12 | State change functions are protected against reentrancy |  | Base |  | [Governance_Base/3.sol](mutations/Governance_Base/3.sol) | ✅ |
| GOV-13 | Functions are not able to receive native tokens |  | Base |  | [Governance_Base/4.sol](mutations/Governance_Base/4.sol) | ✅ |
| GOV-14 | As the snapshot is used only to verify that supply increased when checking the supply cap, the snapshot is disabled if both caps are disabled |  | Base |  |  |  |
| GOV-15 | Snapshot is set only once in batch operations, with cash and total borrow assets, rounded up |  | Base |  |  |  |
| GOV-16 | Anyone can execute view functions |  | View | View functions | [Governance_View/1.sol](mutations/Governance_View/1.sol) | ✅❎ |
| GOV-17 | View functions MUST NOT be protected against reentrancy |  | View | View functions | [Governance_View/2.sol](mutations/Governance_View/2.sol) | ✅❎ |
| GOV-18 | Ensure view functions integrity |  | View | View functions |  | 📝 |
| GOV-19 | View functions don't update state |  | View | View functions |  | ✅ |
| GOV-20 | Governor's ownership can be transferred |  | Ownership | `setGovernorAdmin` | [Governance_Ownership/1.sol](mutations/Governance_Ownership/1.sol) | ✅❎ |
| GOV-21 | The ownership could be revoked by setting the governor to zero address |  | Ownership | `setGovernorAdmin` | [Governance_Ownership/2.sol](mutations/Governance_Ownership/2.sol) | ✅❎ |
| GOV-22 | The fee receiver address can be changed |  | Fees | `setFeeReceiver` |  |  |
| GOV-23 | While distributing fees, the protocol (Euler DAO's) receiver and fee amount are extracted from the protocol config contract |  | Fees | `convertFees` |  |  |
| GOV-24 | If the governor receiver was not set, the protocol gets all fees |  | Fees | `convertFees` |  |  |
| GOV-25 | Protocol's fee share cannot be more than the max protocol fee share (50%) |  | Fees | `convertFees` |  |  |
| GOV-26 | While distributing fees, total shares are decreased by the accumulated fees and accumulated fees are cleared |  | Fees | `convertFees` |  |  |
| GOV-27 | While distributing fees, shares are transferred to governor and protocol fee receiver addresses |  | Fees | `convertFees` |  |  |
| GOV-28 | Fee shares cannot be transferred to the zero address |  | Fees | `convertFees` |  |  |
| GOV-29 | Accumulated fees only increase when some time has passed |  | Fees | `convertFees` |  |  |
| GOV-30 | Fees are retrieved only for the contract itself from the protocol config contract |  | Fees | `convertFees` |  |  |
| GOV-31 | The specified LTV is a fraction between 0 and 1 (scaled by 10,000) |  | Liquidation | `SetLTV` |  |  |
| GOV-32 | Self-collateralization is not allowed |  | Liquidation | `SetLTV` |  |  |
| GOV-33 | The borrow LTV must be lower than or equal to the liquidation LTV |  | Liquidation | `SetLTV` |  |  |
| GOV-34 | Ramp duration can be used only when lowering liquidation LTV |  | Liquidation | `SetLTV` |  |  |
| GOV-35 | The LTV can be set for a collateral asset, including borrow LTV, liquidation LTV, and ramp duration |  | Liquidation | `SetLTV` |  |  |
| GOV-36 | All collateral entries in the vault storage LTV list must be unique |  | Liquidation | `SetLTV` |  |  |
| GOV-37 | The LTV is always initialized when set |  | Liquidation | `SetLTV` |  |  |
| GOV-38 | An empty LTV should not be initialized |  | Liquidation | `SetLTV` |  |  |
| GOV-39 | LTV's timestamp is always less than or equal to the current timestamp |  | Liquidation | `SetLTV` |  |  |
| GOV-40 | Setting the LTV updates the target timestamp to the current time plus the ramp duration |  | Liquidation | `SetLTV` |  |  |
| GOV-41 | Initial liquidation LTV is always the previous liquidation LTV or zero |  | Liquidation | `SetLTV` |  |  |
| GOV-42 | LTV can be increased or decreased immediately |  | Liquidation | `SetLTV` |  |  |
| GOV-43 | Liquidation LTV is calculated dynamically only when ramping is in progress (target timestamp is in the future and liquidation LTV is less than the initial liquidation LTV) |  | Liquidation | `SetLTV` |  |  |
| GOV-44 | Dynamically calculated liquidation LTV is always between the target liquidation LTV and the initial liquidation LTV |  | Liquidation | `SetLTV` |  |  |
| GOV-45 | When ramping is in progress, the time remaining is always less than or equal to the ramp duration |  | Liquidation | `SetLTV` |  |  |
| GOV-46 | LTV setting can be set to 0 |  | Liquidation | `clearLTV` |  |  |
| GOV-47 | Clearing the LTV configuration sets the borrow LTV, liquidation LTV, initial liquidation LTV, timestamp, and ramp duration to zero |  | Liquidation | `clearLTV` |  |  |
| GOV-48 | The maximum liquidation discount can be changed |  | Liquidation | `setMaxLiquidationDiscount` |  |  |
| GOV-49 | The liquidation cool off time can be changed |  | Liquidation | `setLiquidationCoolOffTime` |  |  |
| GOV-50 | The interest rate model can be changed |  | Interest | `setInterestRateModel` |  |  |
| GOV-51 | Cached interest rate is cleared when the interest rate model is set |  | Interest | `setInterestRateModel` |  |  |
| GOV-52 | While calculating the interest rate, the cached value will be used if the interest rate model is not set or the call to the interest rate model was not successful |  | Interest | `setInterestRateModel` |  |  |
| GOV-53 | Calculated interest rate should not be greater than the max allowed interest rate (1,000,000% APY) |  | Interest | `setInterestRateModel` |  |  |
| GOV-54 | Calculated interest rate is logged when the interest rate model or interest fee is set |  | Interest | `setInterestRateModel` |  |  |
| GOV-55 | The interest fee can be changed |  | Interest | `setInterestFee` |  |  |
| GOV-56 | Interest fees in the guaranteed range (0.1% to 100%) are always allowed |  | Interest | `setInterestFee` |  |  |
| GOV-57 | Interest fees outside the guaranteed range must be approved by `protocolConfig` |  | Interest | `setInterestFee` |  |  |
| GOV-58 | The interest fee cannot be greater than `1e4` |  | Interest | `setInterestFee` |  |  |
| GOV-59 | The hook target can be changed |  | Config | `setHookConfig` |  |  |
| GOV-60 | The bitmask indicating hooked operations can be changed |  | Config | `setHookConfig` |  |  |
| GOV-61 | Non-zero hook target must be a valid hook target address |  | Config | `setHookConfig` |  |  |
| GOV-62 | The hook target can be zero when the operation is disabled |  | Config | `setHookConfig` |  |  |
| GOV-63 | The bitmask for hooked operations must be within the valid range |  | Config | `setHookConfig` |  |  |
| GOV-64 | The bitmask indicating config flags can be changed |  | Config | `setConfigFlags` |  |  |
| GOV-65 | The bitmask for config flags must be within the valid range |  | Config | `setConfigFlags` |  |  |
| GOV-66 | The supply cap can be changed |  | Caps | `setCaps` |  |  |
| GOV-67 | The borrow cap can be changed |  | Caps | `setCaps` |  |  |
| GOV-68 | The resolved supply cap must not exceed 2 times the maximum sane amount |  | Caps | `setCaps` |  |  |
| GOV-69 | The resolved borrow cap must not exceed the maximum sane amount |  | Caps | `setCaps` |  |  |
| GOV-70 | When resolving the cap, the exponent is extracted from the least significant 6 bits and the mantissa from the most significant 10 bits, scaled by 100 |  | Caps | `setCaps` |  |  |
| GOV-71 | A zero cap amount can be set, indicating no limit |  | Caps | `setCaps` |  |  |
| GOV-72 | A zero cap always resolves into the maximum `uint256` value |  | Caps | `setCaps` |  |  |

## Vault

| Property | Description | Category | Tag | Entries | Mutation | Status |
| --- | --- | --- | --- | --- | --- | --- |
| VLT-01 | Specific functions require a vault status check |  | Base |  |  |  |
| VLT-02 | Specific functions require a vault and account status check |  | Base |  |  |  |
| VLT-03 | Specific functions execute a hook |  | Base | Specific functions |  |  |
| VLT-04 | Vault's storage can be updated from cache when specific functions are executed |  | Base |  |  |  |
| VLT-05 | State change functions are protected against reentrancy |  | Base |  |  |  |
| VLT-06 | Functions are not able to receive native tokens |  | Base | Functions |  |  |
| VLT-07 | Anyone can execute view functions |  | View | View functions |  |  |
| VLT-08 | Specific view functions are protected against reentrancy, while others are not |  | View | View functions |  |  |
| VLT-09 | Ensure view functions integrity |  | View | View functions |  |  |
| VLT-10 | View functions don't update the state |  | View | View functions |  |  |
| VLT-11 | Each vault holds exactly one creator |  | View | View functions |  |  |
| VLT-12 | Some view functions can be disabled by the governor and MUST return zero |  | Hooks | `maxMint`, `maxWithdraw` |  |  |
| VLT-13 | Functions are considered disabled if a hook has been installed for it and the hook target is zero address |  | Hooks |  |  |  |
| VLT-14 | Hooks are not executed for disabled functions |  | Hooks | Disabled functions |  |  |
| VLT-15 | Each vault holds exactly one underlying asset |  | Convert | `asset` |  |  |
| VLT-16 | Total assets are the sum of the vault's cash and the total borrows converted to assets |  | Convert | `totalAssets` |  |  |
| VLT-17 | Shares maximum amounts during calculations cannot exceed the max sane amount (`uint112` max) |  | Convert | `convertToAssets` |  |  |
| VLT-18 | Assets maximum amounts during calculations cannot exceed the max sane amount (`uint112` max) |  | Convert | `convertToShares` |  |  |
| VLT-19 | Accumulated fees must be converted to assets using rounding down |  | Fees | `accumulatedFeesAssets` |  |  |
| VLT-20 | The number of assets required to deposit is always rounded down |  | Deposit | `previewDeposit` |  |  |
| VLT-21 | Non-zero max deposit assets must not be zero when converted to shares down |  | Deposit | `maxDeposit` |  |  |
| VLT-22 | User's max deposit could be zero even if the operation is enabled |  | Deposit | `maxDeposit` |  |  |
| VLT-23 | Max deposit and max mint are zero when the supply cap is reached |  | Deposit | `maxDeposit`, `maxMint` |  |  |
| VLT-24 | Max deposit must not exceed the supply cap |  | Deposit | `maxDeposit`, `deposit`, `checkVaultStatus` |  |  |
| VLT-25 | Non-zero max deposit assets must correspond to a non-zero shares amount |  | Deposit | `maxDeposit` |  |  |
| VLT-26 | Cash amount must not be greater max sane amount (`uint112` max) |  | Deposit | Cash amount |  |  |
| VLT-27 | Max deposit assets must not be greater than the max sane amount (`uint112` max) minus cash amount |  | Deposit | `maxDeposit` |  |  |
| VLT-28 | Total shares amount must not be greater max sane amount (`uint112` max) |  | Deposit | Total shares amount |  |  |
| VLT-29 | Max mint shares must not be greater than the max sane amount (`uint112` max amount) minus total shares amount |  | Deposit | `maxMint` |  |  |
| VLT-30 | Preview mint should return the amount of assets that will be required in mint |  | Deposit | `previewMint`, `mint` |  |  |
| VLT-31 | Share must not be minted or previewed more than max sane amount (`uint112` max) |  | Deposit | `previewMint`, `mint` |  |  |
| VLT-32 | While minting or previewing mint, shares must be converted to assets using rounding up (all impact of rounding happens in favor of the remaining depositors) |  | Deposit | `previewMint`, `mint` |  |  |
| VLT-33 | Zero assets deposit do nothing and return zero |  | Deposit | `deposit` |  |  |
| VLT-34 | Max `uint256` assets deposit mints using all user's balance assets |  | Deposit | `deposit` |  |  |
| VLT-35 | Zero shares cannot be minted from non-zero assets |  | Deposit | `deposit` |  |  |
| VLT-36 | Deposit and mint transfer assets from the user's account to the current contract's account |  | Deposit | `deposit`, `mint` |  |  |
| VLT-37 | Deposit and mint support permit contract while transferring assets from users' account |  | Deposit | `deposit`, `mint` |  |  |
| VLT-38 | Deposit and mint increase the vault's cash amount |  | Deposit | `deposit`, `mint` |  |  |
| VLT-39 | Shares cannot be deposited, minted or skimmed to the zero address |  | Deposit | `deposit`, `mint`, `skim` |  |  |
| VLT-40 | The user's balance and total vault's shares are increased when shares are deposited, minted or skimmed |  | Deposit | `deposit`, `mint`, `skim` |  |  |
| VLT-41 | Any user's balance is always less than or equal to the total vault's shares plus accumulated fees |  | Deposit | User's balance |  |  |
| VLT-42 | If the balance forwarder is enabled, the balance tracker hook is called when user shares are changed |  | Deposit | `deposit`, `mint`, `skim`, `withdraw`, `redeem` |  |  |
| VLT-43 | Balance forwarder is never executed when the balance forwarder is not enabled |  | Deposit | `deposit`, `mint`, `skim`, `withdraw`, `redeem` |  |  |
| VLT-44 | Balance forwarder can be executed only with specific functions |  | Deposit | `deposit`, `mint`, `skim`, `withdraw`, `redeem` |  |  |
| VLT-45 | The balance tracker hook is called with `forfeitRecentReward` set to `false` when user's balance in increased |  | Deposit | `deposit`, `mint`, `skim` |  |  |
| VLT-46 | The balance tracker hook is called with `forfeitRecentReward` set to `true` only when collateral control is in progress |  | Withdraw | `withdraw`, `redeem` |  |  |
| VLT-47 | Zero mint amount do nothing and return zero |  | Deposit | `mint` |  |  |
| VLT-48 | Shares are converted to assets using rounding up during minting |  | Deposit | `mint` |  |  |
| VLT-49 | Only specific functions can increase a user's balance |  | Deposit | `deposit`, `mint`, `skim` |  |  |
| VLT-50 | Total shares can be changed only when a user's balance changes (fee converting is an exception) |  | Deposit | `deposit`, `mint`, `skim`, `redeem`, `withdraw` |  |  |
| VLT-51 | Excess assets available to skim are calculated as the vault's balance minus the vault's cash |  | Deposit | `skim` |  |  |
| VLT-52 | Max `uint256` requested to skim assets means using the entire excess vault's balance |  | Deposit | `skim` |  |  |
| VLT-53 | Skimming more assets than the excess vault's internal balance is not allowed |  | Deposit | `skim` |  |  |
| VLT-54 | Operating with zero assets or zero shares is not allowed |  | Deposit | `skim` |  |  |
| VLT-55 | Skimmed assets are converted to shares, rounded down |  | Deposit | `skim` |  |  |
| VLT-56 | Skimmed assets increase the vault's cash balance |  | Deposit | `skim` |  |  |
| VLT-57 | The quantity of assets that can be redeemed for a given number of shares is always rounded down |  | Withdraw | `previewRedeem` |  |  |
| VLT-58 | The number of shares required to withdraw a given quantity of assets is rounded up |  | Withdraw | `previewWithdraw` |  |  |
| VLT-59 | Max withdraw assets and max redeem shares must be zero when the user balance is zero |  | Withdraw | `maxWithdraw`, `maxRedeem` |  |  |
| VLT-60 | When an account has a controller enabled (ie, has an active borrow), calling `maxWithdraw` and `maxRedeem` on the account's collateral vaults must return `0` |  | Withdraw | `maxWithdraw`, `maxRedeem` |  |  |
| VLT-61 | Max redeem shares amount must not be greater than the user's available balance |  | Withdraw | `maxRedeem` |  |  |
| VLT-62 | Max redeem shares amount must not be greater than the vault's available cash amount, rounded down |  | Withdraw | `maxRedeem` |  |  |
| VLT-63 | Non-zero max redeem shares amount must correspond to a non-zero assets amount, rounded down |  | Withdraw | `maxRedeem` |  |  |
| VLT-64 | Max withdraw assets must correspond to max redeem shares, converted to assets and rounded down |  | Withdraw | `maxWithdraw`, `maxRedeem` |  |  |
| VLT-65 | Zero withdraw amount do nothing and return zero |  | Withdraw | `withdraw` |  |  |
| VLT-66 | Withdraw asset amounts are converted to shares, rounding up |  | Withdraw | `withdraw` |  |  |
| VLT-67 | Withdraw and redeem are reverted if the vault's cash is insufficient |  | Withdraw | `withdraw`, `redeem` |  |  |
| VLT-68 | Allowance is not decreased if the amount is zero or if the owner is the spender |  | Withdraw | `withdraw`, `redeem` |  |  |
| VLT-69 | A `uint256` maximum allowance means unlimited allowance, so it is not decreased during operations |  | Withdraw | `withdraw`, `redeem` |  |  |
| VLT-70 | The operation reverts if the allowance is less than the required amount |  | Withdraw | `withdraw`, `redeem` |  |  |
| VLT-71 | The user's allowance for the spender is updated after being decreased |  | Withdraw | `withdraw`, `redeem` |  |  |
| VLT-72 | Withdraw and redeem could not be processed if the allowance is insufficient |  | Withdraw | `withdraw`, `redeem` |  |  |
| VLT-73 | Withdraw and redeem reverts if the user's original balance is less than the required amount |  | Withdraw | `withdraw`, `redeem` |  |  |
| VLT-74 | The user's balance and total vault's shares are decreased when shares are withdrawn or redeemed |  | Withdraw | `withdraw`, `redeem` |  |  |
| VLT-75 | Zero redeem amount do nothing and return zero |  | Withdraw | `redeem` |  |  |
| VLT-76 | Max `uint256` shares redeem withdraw using all user's balance assets |  | Withdraw | `redeem` |  |  |
| VLT-77 | Zero assets cannot be redeemed from non-zero shares |  | Withdraw | `redeem` |  |  |
| VLT-78 | Withdraw and redeem transfer assets from the vault to the receiver |  | Withdraw | `withdraw`, `redeem` |  |  |
| VLT-79 | Withdraw and redeem check `transfer` result while transferring to the receiver |  | Withdraw | `withdraw`, `redeem` |  |  |
| VLT-80 | Withdraw and redeem decrease the vault's cash amount |  | Withdraw | `withdraw`, `redeem` |  |  |
| VLT-81 | Assets cannot be withdrawn to the zero address |  | Withdraw | `withdraw`, `redeem` |  |  |
| VLT-82 | Assets cannot be withdrawn or redeemed to sub-accounts when asset itself is NOT compatible with EVC |  | Withdraw | `withdraw`, `redeem` |  |  |

## Borrowing

| Property | Description | Category | Tag | Entries | Mutation | Status |
| --- | --- | --- | --- | --- | --- | --- |
| BRW-01 | Specific functions require a vault status check |  | Base |  |  |  |
| BRW-02 | Specific functions require a vault and account status check |  | Base |  |  |  |
| BRW-03 | Specific functions execute a hook |  | Base |  |  |  |
| BRW-04 | Vault's storage can be updated from cache when specific functions are executed |  | Base |  |  |  |
| BRW-05 | State change functions are protected against reentrancy |  | Base |  |  |  |
| BRW-06 | Functions are not able to receive native tokens |  | Base | Functions |  |  |
| BRW-07 | Anyone can execute view functions |  | View | View functions |  |  |
| BRW-08 | Specific view functions are protected against reentrancy, while others are not |  | View | View functions |  |  |
| BRW-09 | View functions don't update state |  | View | View functions |  |  |
| BRW-10 | Ensure view functions integrity |  | View | View functions |  |  |
| BRW-11 | Total borrows are converted to assets using rounding up |  | View | `totalBorrows` |  |  |
| BRW-12 | Total borrows are retrieved directly without conversion |  | View | `totalBorrowsExact` |  |  |
| BRW-13 | User's debt is retrieved and converted to assets using rounding up |  | View | `debtOf` |  |  |
| BRW-14 | User's debt is retrieved in underlying units scaled up by internal debt precision |  | View | `debtOfExact` |  |  |
| BRW-15 | Interest rate is calculated by invoking the `computeInterestRateView` function on the interest rate model |  | View | `interestRate` |  |  |
| BRW-16 | While calculating the interest rate, the cached value will be used if the interest rate model is not set or the call to the interest rate model was not successful |  | View | `interestRate` |  |  |
| BRW-17 | Calculated interest rate should not be greater than max allowed interest rate (1,000,000% APY) |  | View | `interestRate` |  |  |
| BRW-18 | `DToken` contract address can be calculated from the vault's address and the nonce `1` |  | View | `DToken` |  |  |
| BRW-19 | Functions are considered disabled if a hook has been installed for it and the hook target is zero address |  | Hooks | `isOperationDisabled` |  |  |
| BRW-20 | Hooks are not executed for disabled functions |  | Hooks | Disabled functions |  |  |
| BRW-21 | Max `uint256` max assets to borrow means using all vault's available tokens |  | Borrow | `borrow` |  |  |
| BRW-22 | Users cannot borrow assets exceeding the max sane amount (`uint112` max) |  | Borrow | `borrow` |  |  |
| BRW-23 | Zero assets borrow do nothing and return zero |  | Borrow | `borrow` |  |  |
| BRW-24 | Users cannot borrow more assets than the available cash in the vault |  | Borrow | `borrow` |  |  |
| BRW-25 | While borrowing, actual user's debt is calculated by multiplying the vault's interest accumulator and dividing by the user's interest accumulator |  | Borrow | `borrow` |  |  |
| BRW-26 | The user's interest accumulator is always less than or equal to the vault's interest accumulator |  | Borrow | User's interest accumulator |  |  |
| BRW-27 | The user's debt is always greater than or equal to the previous debt |  | Borrow | `borrow` |  |  |
| BRW-28 | The user's debt, calculated with the interest accumulator, is always greater than or equal to the previous debt |  | Borrow | `borrow` |  |  |
| BRW-29 | The user's debt is updated with the new debt value calculated while borrowing |  | Borrow | `borrow` |  |  |
| BRW-30 | The user's interest accumulator is updated to match the vault's interest accumulator |  | Borrow | `borrow` |  |  |
| BRW-31 | Cache and storage total borrows in the vault are increased by the borrowed amount |  | Borrow | `borrow` |  |  |
| BRW-32 | Borrowing events are logged with the account, borrowed assets, previous debt, and current debt |  | Borrow | `borrow`, `logBorrow` |  |  |
| BRW-33 | The amount of assets borrowed is returned to the user |  | Borrow | `borrow` |  |  |
| BRW-34 | Vault's total borrows are always greater than or equal to user's borrow |  | Borrow | User's borrow |  |  |
| BRW-35 | When a user's debt changes, the vault's total borrows must also change |  | Borrow | User's debt |  |  |
| BRW-36 | Borrowed assets are transferred to the receiver after increasing the user's debt |  | Borrow | `borrow` |  |  |
| BRW-37 | Max `uint256` max assets to repay means using the total user's debt |  | Repay | `repay` |  |  |
| BRW-38 | While repaying, the total user's debt is calculated by multiplying the vault's interest accumulator and dividing by the user's interest accumulator, converted to assets, rounded up |  | Repay | `repay` |  |  |
| BRW-39 | Users cannot repay assets exceeding the max sane amount (`uint112` max) |  | Repay | `repay`, `repayWithShares` |  |  |
| BRW-40 | Zero assets repaying does nothing and returns zero |  | Repay | `repay` |  |  |
| BRW-41 | While repaying, assets are transferred from user's account to vault's account |  | Repay | `repay` |  |  |
| BRW-42 | While repaying, the actual user's debt is calculated by multiplying the vault's interest accumulator and dividing by the user's interest accumulator |  | Repay | `repay` |  |  |
| BRW-43 | While repaying, the total user's debt in assets is rounded up |  | Repay | `repay` |  |  |
| BRW-44 | The repayment amount must not exceed the user's total owed debt, rounded up |  | Repay | `repay` |  |  |
| BRW-45 | While repaying, the user's debt is updated to reflect the new amount after repayment |  | Repay | `repay` |  |  |
| BRW-46 | While repaying, the user's interest accumulator is updated to match the vault's interest accumulator |  | Repay | `repay` |  |  |
| BRW-47 | While repaying, cache and storage total borrows in the vault are decreased by the repaid amount |  | Repay | `repay` |  |  |
| BRW-48 | While repaying, total borrows underflow is not possible |  | Repay | `repay` |  |  |
| BRW-49 | Repaying events are logged with the account, repaid assets, previous debt, and current debt |  | Repay | `borrow` |  |  |
| BRW-50 | The amount of assets repaid is returned as a function result |  | Repay | `repay` |  |  |
| BRW-51 | Zero owed debt repaying does nothing and returns zero |  | RepayWithShares | `repayWithShares` |  |  |
| BRW-52 | Max `uint256` assets to repay with shares means to repay the debt in full or up to the available share balance |  | RepayWithShares | `repayWithShares` |  |  |
| BRW-53 | While repaying with all available shares, assets are calculated rounded down, in favor of the vault |  | RepayWithShares | `repayWithShares` |  |  |
| BRW-54 | While repaying with shares, required assets are calculated rounded up, in favor of the vault |  | RepayWithShares | `repayWithShares` |  |  |
| BRW-55 | Zero assets repaying with shares does nothing and returns zero |  | RepayWithShares | `repayWithShares` |  |  |
| BRW-56 | The repayment amount must not exceed the user's total owed debt, required shares are rounded up |  | RepayWithShares | `repayWithShares` |  |  |
| BRW-57 | The user's balance and vault's total shares are decreased when shares are repaid |  | RepayWithShares | `repayWithShares` |  |  |
| BRW-58 | The user's debt is decreased when assets are repaid with shares |  | RepayWithShares | `repayWithShares` |  |  |
| BRW-59 | Repaying with shares function returns the number of shares burned and the amount of debt repaid in assets |  | RepayWithShares | `repayWithShares` |  |  |
| BRW-60 | The user cannot transfer debt to themselves |  | PullDebt | `pullDebt` |  |  |
| BRW-61 | Max `uint256` assets to pull debt means transferring all the account's debt |  | PullDebt | `pullDebt` |  |  |
| BRW-62 | Users cannot pull debt with assets exceeding the max sane amount (`uint112` max) |  | PullDebt | `pullDebt` |  |  |
| BRW-63 | While pulling debt, zero assets amount does nothing and returns zero |  | PullDebt | `pullDebt` |  |  |
| BRW-64 | If the amount was rounded up or dust is left over, the exact amount owed is transferred |  | PullDebt | `PullDebt` |  |  |
| BRW-65 | While pulling debt, if the amount exceeds the owed debt, the transaction reverts |  | PullDebt | `PullDebt` |  |  |
| BRW-66 | While pulling debt, the from-account's debt is decreased by the transferred amount |  | PullDebt | `pullDebt`, `PullDebt` |  |  |
| BRW-67 | While pulling debt, the target account's debt is increased by the transferred amount |  | PullDebt | `pullDebt`, `PullDebt` |  |  |
| BRW-68 | While pulling debt, repaying event is logged with the account, repaid assets, previous debt, and current debt |  | PullDebt | `borrow` |  |  |
| BRW-69 | While pulling debt, borrowing event is logged with the account, borrowed assets, previous debt, and current debt |  | PullDebt | `borrow` |  |  |
| BRW-70 | The amount of debt pulled is returned in asset units |  | PullDebt | `pullDebt` |  |  |
| BRW-71 | The flash loan operation calls a hook if configured, passing the operation code and account |  | FlashLoan | `flashLoan` |  |  |
| BRW-72 | The original balance of the vault's assets is recorded before the flash loan operation |  | FlashLoan | `flashLoan` |  |  |
| BRW-73 | The requested amount of assets is transferred to the account initiating the flash loan |  | FlashLoan | `flashLoan` |  |  |
| BRW-74 | During a flash loan, the borrower's contract must implement the `onFlashLoan` callback to execute logic with the borrowed assets |  | FlashLoan | `flashLoan` |  |  |
| BRW-75 | Flash loan must be repaid in full before the callback returns, or the transaction reverts |  | FlashLoan | `flashLoan` |  |  |