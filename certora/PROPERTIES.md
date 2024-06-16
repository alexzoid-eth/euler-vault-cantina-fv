# Properties

**Category**: List of properties following the categorization by [Certora](https://github.com/Certora/Tutorials/blob/master/06.Lesson_ThinkingProperties/Categorizing_Properties.pdf):

- High Level
- Valid State
- State Transition
- Variable Transition
- Unit Test

**Mutation**: Path to the mutated file used to prove the property

## Common

These properties are global and include invariants and parametric rules, designed to be tested across multiple contracts: `Borrowing`, `Vault` (including `Token`), `Governance`, `Liquidation`, and `RiskManager`. 

| Property | Description | Category | Mutation |
| --- | --- | --- | --- |
| COM-01 | Accumulated fees MUST result in an increase in the total shares of the vault |  |  |
| COM-02 | Snapshot MUST NOT be used when it is not initialized |  |  |
| COM-03 | Snapshot cash MUST set from storage cash or reset |  |  |
| COM-04 | Clearing accumulated fees MUST move the fees to one or two designated fee receiver addresses |  |  |
| COM-05 | Functions are not able to receive native tokens |  |  |
| COM-06 | Change interest accumulator or accumulated fees accrued MUST set last interest accumulator timestamp |  |  |
| COM-07 | Interest accumulator is updated only when last interest accumulator time changed |  |  |
| COM-08 | The vault's cash changes without assets transfer only when surplus assets available |  |  |
| COM-09 | Transferring assets from the vault MUST decrease the available cash balance |  |  |
| COM-10 | Changes in the cash balance MUST correspond to changes in the total shares |  |  |
| COM-11 | Accumulated fees MUST NOT decrease unless they are being reset to zero |  |  |
| COM-12 | Fees are retrieved only for the contract itself from the protocol config contract |  |  |
| COM-13 | Ramp duration can be used only when lowering liquidation LTV |  |  |
| COM-14 | Collateral LTV MUST NOT be removed completely |  |  |
| COM-15 | Interest accumulator always grows |  |  |
| COM-16 | User interest accumulator always grows |  |  |
| COM-17 | User interest accumulator set always when user borrow changes |  |  |
| COM-18 | Interest accumulator cannot overflow |  |  |
| COM-19 | Interest rate computed always for the current contract |  |  |
| COM-20 | Transfer assets to sub-account allowed only when asset is compatible with EVC |  |  |
| COM-21 | Creator is unchanged |  |  |
| COM-22 | Accumulated fees unchanged when interest fees zero |  |  |
| COM-23 | Allowance unchanged when user redeem shares to their own account |  |  |
| COM-24 | Allowance decrease (unless equal to max_uint256) when user redeem from another account |  |  |
| COM-25 | Only the owner can increase allowance |  |  |
| COM-26 | Balance forwarder must be executed on any share movements when set |  |  |
| COM-27 | User borrow changes must be reflected in total borrows |  |  |
| COM-28 | Increase or decrease user borrow transfers vault's assets out or in |  |  |
| COM-29 | Any shares or borrows movements required account health check |  |  |
| COM-30 | Increase shares or increase borrows MUST execute VAULT health check |  |  |

The properties below are categorized as valid state properties, which can be used to assume a valid storage state in other high-level properties. 

| Property | Description | Category | Mutation |
| --- | --- | --- | --- |
| ST-01 | Vault MUST NOT be deinitialized | Valid State | |
| ST-02 | Uninitialized snapshot MUST be reset | Valid State | |
| ST-03 | Snapshot stamp MUST be always equal to 1 | Valid State | |
| ST-04 | Last interest accumulator timestamp set when positive accumulated fees | Valid State | |
| ST-05 | Last interest accumulator timestamp MUST NOT be in the future | Valid State | |
| ST-06 | Cash amount MUST NOT be less than the ERC20 assets stored in the current contract | Valid State | |
| ST-07 | Max supply and borrow caps limitations | Valid State | |
| ST-08 | Hooks limitations | Valid State | |
| ST-09 | Accumulated fees limitations | Valid State | |
| ST-10 | Shares cannot be transferred to the zero address | Valid State | |
| ST-11 | Self-collateralization is not allowed | Valid State | |
| ST-12 | The borrow LTV MUST be lower than or equal to the liquidation LTV | Valid State | |
| ST-13 | The LTV is always initialized when set | Valid State | |
| ST-14 | LTV with zero timestamp should not be initialized | Valid State | |
| ST-15 | LTV's timestamp is always less than or equal to the current timestamp | Valid State | |
| ST-16 | LTV's timestamp MUST be in the future only when ramping set | Valid State | |
| ST-17 | Initialized LTV exists in collaterals list | Valid State | |
| ST-18 | Zero timestamp means the LTV is cleared or not set yet | Valid State | |
| ST-19 | Config parameters are scaled to `1e4` | Valid State | |
| ST-20 | All collateral entries in the vault storage LTV list MUST be unique | Valid State | |
| ST-21 | The specified LTV is a fraction between 0 and 1 (scaled by 10,000) | Valid State | |
| ST-22 | Liquidation LTV is calculated dynamically only when ramping is in progress and always between the target liquidation LTV and the initial liquidation LTV | Valid State | |
| ST-23 | When ramping is in progress, the time remaining is always less than or equal to the ramp duration | Valid State | |
| ST-24 | Config flags limitations | Valid State |  |
| ST-25 | Transfer assets to zero address not allowed | Valid State |  |
| ST-26 | Interest rate has a maximum limit of 1,000,000 APY |  |
| ST-27 | User interest accumulator always less or equal vault interest accumulator | Valid State | |
| ST-28 | User's interest accumulator set when non-zero owed | Valid State |  |
| ST-29 | Interest accumulator is scaled by 1e27 | Valid State |  |
| ST-30 | Interest rate zero when interest rate model contract is not set| Valid State |  |
| ST-31 | Owner and spender in allowances should differ | Valid State |  |

## Vault_1

| Property | Description | Category | Mutation |
| --- | --- | --- | --- |
| VL1-01 | Accumulated fees MUST always be less than or equal to total shares |  |  |
| VL1-02 | User balance plus accumulated fees MUST always be equal to the total shares (with only 1 user) |  |  |
| VL1-03 | Sum of three users' balance MUST always be equal to the total shares (with only 3 users) |  |  |
| VL1-04 | The vault's cash changes MUST be accompanied by assets transfer (when no surplus assets available) |  |  |
| VL1-05 | Changes in the cash balance MUST correspond to changes in user's shares |  |  |
| VL1-06 | Snapshot is disabled if both caps are disabled (at low-level set to 0, but resolved to max_uint256) |  |  |
| VL1-07 | When user deposit assets and redeem shares, all rounding MUST be in favor of vault |  |  |

## Borrowing_1

| Property | Description | Category | Mutation |
| --- | --- | --- | --- |

## Governance_1

| Property | Description | Category | Mutation |
| --- | --- | --- | --- |
| GV1-01 | Only the governor can invoke methods that modify the configuration of the vault |  |  |
| GV1-02 | Only one governor can exist at one time |  |  |
| GV1-03 | Governor's ownership can be transferred |  |  |
| GV1-04 | The ownership could be revoked by setting the governor to zero address |  |  |
| GV1-05 | The fee receiver address can be changed |  |  |
| GV1-06 | While distributing fees, external protocol config contract is used |  | [Governance_1/1.sol](./mutations/Governance_1/1.sol) |
| GV1-07 | Update the protocol (Euler DAO's) receiver and fee amount for the current contract MUST affect the state |  |  |
| GV1-08 | Update the protocol (Euler DAO's) receiver and fee amount for another contract MUST NOT affect the state |  |  |
| GV1-09 | The governor fee receiver can be disabled |  |  |
| GV1-10 | If the governor receiver was not set, the protocol gets all fees |  |  |
| GV1-11 | Protocol's fee share cannot be more than the max protocol fee share (50%) |  |  |
| GV1-12 | While distributing fees, total shares MUST NOT change and accumulated fees are cleared |  |  |
| GV1-13 | While distributing fees, shares are transferred to governor and protocol fee receiver addresses |  |  |
| GV1-14 | Accumulated fees only increase when some time has passed |  |  |
| GV1-15 | The LTV can be set for a collateral asset, including borrow LTV, liquidation LTV, and ramp duration |  |  |
| GV1-16 | LTV can be increased or decreased immediately |  |  |
| GV1-17 | Initial liquidation LTV is always the previous liquidation LTV or greater than liquidation LTV when ramping |  |  |
| GV1-18 | Non-governor methods MUST be accessible to any callers |  |  |

## RiskManager_1

| Property | Description | Category | Mutation |
| --- | --- | --- | --- |
| RM1-01 | Total shares and total borrows limitations | | |

## Liquidation_1

| Property | Description | Category | Mutation |
| --- | --- | --- | --- |
| LQ-1 | Liquidation operations are prohibited until the cool-down period has passed |  |  |

## Funcs

These properties test the execution behavior common to all contracts. Each specification corresponds to a specific contract and includes properties relevant to its functionality.

### Vault_Funcs

| Property | Description | Category | Mutation |
| --- | --- | --- | --- |
| VLF-01 | Specific functions require a vault status check |  |  |
| VLF-02 | Specific functions require a vault and account status check |  |  |
| VLF-05 | State change functions are protected against reentrancy |  |  |
| VLF-07 | Anyone can execute view functions |  |  |
| VLF-08 | Specific view functions are protected against reentrancy, while others are not |  |  |
| VLF-10 | View functions don't update the state |  |  |

### Governance_Funcs

| Property | Description | Category | Mutation |
| --- | --- | --- | --- |
| GVF-01 | Specific functions can modify state |  | [Governance_Funcs/1.sol](./mutations/Governance_Funcs/1.sol) |
| GVF-02 | Possibility of modifying state |  |  |
| GVF-03 | Specific functions require a vault status check |  | [Governance_Funcs/2.sol](./mutations/Governance_Funcs/2.sol) |
| GVF-04 | State change functions are protected against reentrancy |  | [Governance_Funcs/3.sol](./mutations/Governance_Funcs/3.sol) |
| GVF-05 | Anyone can execute view functions |  | [Governance_Funcs/6.sol](./mutations/Governance_Funcs/6.sol) |
| GVF-06 | View functions MUST NOT be protected against reentrancy |  | [Governance_Funcs/5.sol](./mutations/Governance_Funcs/5.sol) |
| GVF-07 | View functions don't update state |  |  |