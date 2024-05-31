# Properties

List of properties following the categorization by [Certora](https://github.com/Certora/Tutorials/blob/master/06.Lesson_ThinkingProperties/Categorizing_Properties.pdf):

- High Level
- Valid States
- State Transitions
- Variable Transitions
- Unit Tests

### Base

- As the snapshot is used only to verify that supply increased when checking the supply cap, the snapshot is disabled if both caps are disabled (`initOperation`)
- Snapshot is set only once in batch operations, with cash and total borrow assets, rounded up (`initOperation`)

### Governance

#### GOV-1-Execution

##### GOV-1-governorOnly
- Only the governor can invoke methods that modify the configuration of the vault
- Only one governor can exist at one time 
- When the sender is `EVC`, the governor's address is extracted from the operation's current account on behalf
- Governor's functions cannot be executed from `EVC` when the authenticated account is a governor's sub-account
- Governor's functions cannot be executed from `EVC` when an operator is authenticated
- Governor's functions cannot be executed from `EVC` when control collateral is in progress
- When the sender is not `EVC`, the governor's address is set as `msg.sender`
- Governor's functions don't process any additional check in `EVC` when the sender is not `EVC`
##### GOV-1-Base
- Specific functions requires a vault status check
- Specific functions executes a hook
- Vault's storage can be updated from cache when specific functions are executed
- State change functions are protected against reentrancy
- Functions are not able to receive native tokens
##### GOV-1-View
- Anyone can execute view functions and convert fees
- View functions are not protected against reentrancy
- Ensure view functions integrity 
- View function don't update state

#### GOV-2-Ownership

##### GOV-2-setGovernorAdmin
- Governor's ownership can be transferred 
- The ownership could be revoked by setting the governor to zero address

#### GOV-3-Fees

##### GOV-3-setFeeReceiver
- The fee receiver address can be changed
##### GOV-3-convertFees
- While distributing fees, the protocol (Euler DAO's) receiver and fee amount are extracted from the protocol config contract
- If the governor receiver was not set, the protocol gets all fees
- Protocol's fee share cannot be more than the max protocol fee share (50%)
- While distributing fees, total shares are decreased by the accumulated fees and accumulated fees are cleared
- While distributing fees, share are transferred to governor and protocol fee receiver addresses 
- Fee shares cannot be transferred to the zero address
- Accumulated fees only increase when some time has passed
- Fees are retrieved only for the contract itself from the protocol config contract

#### GOV-4-Liquidation

##### GOV-4-SetLTV
- The specified LTV is a fraction between 0 and 1 (scaled by 10,000)
- Self-collateralization is not allowed
- The borrow LTV must be lower than or equal to the the liquidation LTV
- Ramp duration can be used only when lowering liquidation LTV
- The LTV can be set for a collateral asset, including borrow LTV, liquidation LTV, and ramp duration
- All collateral entries in the vault storage LTV list are unique
- The LTV is always initialized when set
- An empty LTV should not be initialized
- LTV's timestamp is always less than or equal to the current timestamp
- Setting the LTV updates the target timestamp to the current time plus the ramp duration
- Initial liquidation LTV is always the previous liquidation LTV or zero
- LTV can be increased or decreased immediately
- Liquidation LTV is calculated dynamically only when ramping is in progress (target timestamp is in the future and liquidation LTV is less than the initial liquidation LTV)
- Dynamically calculated liquidation LTV is always between the target liquidation LTV and the initial liquidation LTV
- When ramping is in progress, the time remaining is always less than or equal to the ramp duration.
##### GOV-4-clearLTV
- LTV setting can be set to 0
- Clearing the LTV configuration sets the borrow LTV, liquidation LTV, initial liquidation LTV, timestamp and ramp duration to zero
##### GOV-4-setMaxLiquidationDiscount
- The maximum liquidation discount can be changed
##### GOV-4-setLiquidationCoolOffTime
- The liquidation cool off time can be changed

#### GOV-5-Interest

##### GOV-5-setInterestRateModel
- The interest rate model can be changed
- Cached interest rate is cleared when the interest rate model is set
- While calculating the interest rate, the cached value will be used if the interest rate model is not set or the call to the interest rate model was not successful
- Calculated interest rate should not be greater than max allowed interest rate (1,000,000% APY)
- Calculated interest rate is logged when the interest rate model or interest fee is set
##### GOV-5-setInterestFee
- The interest fee can be changed
- Interest fees in the guaranteed range (0.1% to 100%) are always allowed
- Interest fees outside the guaranteed range must be approved by `protocolConfig`
- The interest fee cannot be greater than `1e4`

#### GOV-6-Config

##### GOV-6-setHookConfig
- The hook target can be changed
- The bitmask indicating hooked operations can be changed
- Non-zero hook target must be a valid hook target address
- The hook target can be zero when the operation is disabled
- The bitmask for hooked operations must be within the valid range

##### GOV-6-ConfigFlags
- The bitmask indicating config flags can be changed
- The bitmask for config flags must be within the valid range

#### GOV-7-Caps

##### GOV-7-setCaps
- The supply cap can be changed
- The borrow cap can be changed
- The resolved supply cap must not exceed 2 times the maximum sane amount
- The resolved borrow cap must not exceed the maximum sane amount
- When resolving the cap, the exponent is extracted from the least significant 6 bits and the mantissa from the most significant 10 bits, scaled by 100
- A zero cap amount can be set, indicating no limit
- A zero cap always resolves into the maximum `uint256` value

### Vault

#### VLT-1-Execution

##### VLT-1-Base
- Specific functions requires a vault status check
- Specific functions requires a vault and account status check
- Specific functions executes a hook
- Vault's storage can be updated from cache when specific functions are executed
- State change functions are protected against reentrancy
- Functions are not able to receive native tokens
##### VLT-1-View
- Anyone can execute view functions
- Specific view functions are protected against reentrancy, while others are not
- Ensure view functions integrity 
- View functions don't update the state
- Each vault holds exactly one creator
##### VLT-1-Hooks
- Some view functions can be disabled by the governor and MUST return zero (`maxMint`, `maxWithdraw` ...)
- An functions is considered disabled if a hook has been installed for it and the hook target is zero address (`isOperationDisabled`)
- Hooks are not executed for disabled functions

#### VLT-2-AssetsShares
- Each vault holds exactly one underlying asset (`asset`)
- Total assets are the sum of the vault's cash and the total borrows converted to assets (`totalAssets`)
- Shares maximum amounts during calculations cannot exceed the max sane amount (uint112 max) (`convertToAssets`)
- Assets maximum amounts during calculations cannot exceed the max sane amount (uint112 max) (`convertToShares`)
#### VLT-2-Fees
- Accumulated fees must be converted to assets using rounding down (`accumulatedFeesAssets`)
#### VLT-2-DepositMintSkim
- The number of assets required to deposit is always rounded down (`previewDeposit`)
- Non-zero max deposit assets must not be zero when converted to shares down (`maxDeposit`)
- User's max deposit could be zero even if the operation is enabled (`maxDeposit`)
- Max deposit and max mint are zero when the supply cap is reached (`maxDeposit`, `maxMint`)
- Max deposit must not exceed the supply cap (`maxDeposit`, `deposit`, `checkVaultStatus`)
- Non-zero max deposit assets must correspond to a non-zero shares amount (`maxDeposit`)
- Cash amount must not be greater max sane amount (uint112 max)
- Max deposit assets must not be greater than the max sane amount (uint112 max) minus cash amount (`maxDeposit`)
- Total shares amount must not be greater max sane amount (uint112 max)
- Max mint shares must not be greater than the max sane amount (uint112 max amount) minus total shares amount (`maxMint`)
- Preview mint should return the amount of assets that will be required in mint (`previewMint`, `mint`)
- Share must not be minted or previewed more than max sane amount (uint112 max) (`previewMint`, `mint`)
- While minting or previewing mint, shares must be converted to assets using rounding up (all impact of rounding happens in favor of the remaining depositors) (`previewMint`, `mint`)
- Zero assets deposit do nothing and return zero (`deposit`)
- Max `uint256` assets deposit mints using all user's balance assets (`deposit`)
- Zero shares cannot be minted from non-zero assets (`deposit`)
- Deposit and mint transfer assets from the user's account to the current contract's account (`deposit`, `mint`)
- Deposit and mint support permit contract while transferring assets from users' account (`deposit`, `mint`)
- Deposit and mint increase the vault's cash amount (`deposit`, `mint`)
- Shares cannot be deposited or minted to the zero address (`deposit`, `mint`)
- The user's balance and total vault's shares are updated when shares are deposited or minted (`deposit`, `mint`)
- Any user's balance is always less than or equal to the total vault's shares plus accumulated fees
- If the balance forwarder is enabled, the balance tracker hook is called when shares are deposited or minted (`deposit`, `mint`)
- Zero mint amount do nothing and return zero (`mint`)
- Shares are converted to assets using rounding up during minting (`mint`)
- Only specific functions can increase a user's balance (`deposit`, `mint`, `skim`)
- Total shares can be changed only when a user's balance changes (fee converting is an exception) (`deposit`, `mint`, `skim`, `redeem`, `withdraw`)
- Directly send tokens can be recovered by anyone 
#### VLT-2-WithdrawRedeem
- The quantity of assets that can be redeemed for a given number of shares is always rounded down (`previewRedeem`)
- The number of shares required to withdraw a given quantity of assets is rounded up (`previewWithdraw`)
- Max withdraw assets and max redeem shares must be zero when the user balance is zero (`maxWithdraw`, `maxRedeem`)
- When an account has a controller enabled (ie, has an active borrow), calling `maxWithdraw` and `maxRedeem` on the account's collateral vaults must return `0` (`maxWithdraw`, `maxRedeem`)
- Max redeem shares amount must not be greater than the user's available balance (`maxRedeem`)
- Max redeem shares amount must not be greater than the vault's available cash amount, rounded down (`maxRedeem`)
- Non-zero max redeem shares amount must correspond to a non-zero assets amount, rounded down (`maxRedeem`)
- Max withdraw assets must correspond to max redeem shares, converted to assets and rounded down (`maxWithdraw`, `maxRedeem`)
