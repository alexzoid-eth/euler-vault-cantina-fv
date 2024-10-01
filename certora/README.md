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
| COM-01 | Accumulated fees MUST result in an increase in the total shares of the vault | State Transition |  |
| COM-02 | Snapshot MUST NOT be used when it is not initialized | Valid State |  |
| COM-03 | Snapshot cash MUST set from storage cash or reset | State Transition |  |
| COM-04 | Clearing accumulated fees MUST move the fees to one or two designated fee receiver addresses | Variable Transition |  |
| COM-05 | Functions are not able to receive native tokens | State Transition |  |
| COM-06 | Change interest accumulator or accumulated fees accrued MUST set last interest accumulator timestamp | State Transition |  |
| COM-07 | Interest accumulator is updated only when last interest accumulator time changed | State Transition |  |
| COM-08 | The vault's cash changes without assets transfer only when surplus assets available | State Transition |  |
| COM-09 | Transferring assets from the vault MUST decrease the available cash balance | High Level |  |
| COM-10 | Changes in the cash balance MUST correspond to changes in the total shares | High Level | [Borrowing/Borrowing_0.sol](./mutations/Borrowing/Borrowing_0.sol) |
| COM-11 | Accumulated fees MUST NOT decrease unless they are being reset to zero | Variable Transition |  |
| COM-12 | Fees are retrieved only for the contract itself from the protocol config contract | State Transition |  |
| COM-13 | Ramp duration can be used only when lowering liquidation LTV | High Level |  |
| COM-14 | Collateral LTV MUST NOT be removed completely | Valid State |  |
| COM-15 | Interest accumulator always grows | Variable Transition |  |
| COM-16 | User interest accumulator always grows | Variable Transition |  |
| COM-17 | User interest accumulator set always when user borrow changes | Variable Transition |  |
| COM-18 | Interest accumulator cannot overflow | Variable Transition |  |
| COM-19 | Interest rate computed always for the current contract | State Transition |  |
| COM-20 | Transfer assets to sub-account allowed only when asset is compatible with EVC | State Transition |  |
| COM-21 | Creator is unchanged | Valid State |  |
| COM-22 | Accumulated fees unchanged when interest fees zero | Valid State |  |
| COM-23 | Allowance unchanged when user redeem shares to their own account | State Transition |  |
| COM-24 | Allowance decrease (unless equal to max_uint256) when user redeem from another account | State Transition |  |
| COM-25 | Only the owner can increase allowance | State Transition |  |
| COM-26 | Balance forwarder must be executed on any share movements when set | High Level |  |
| COM-27 | User borrow changes must be reflected in total borrows | Valid State |  |
| COM-28 | Increase or decrease user borrow transfers vault's assets out or in | High Level |  |
| COM-29 | Any shares or borrows movements required account health check | High Level |  |
| COM-30 | Increase shares or increase borrows MUST execute VAULT health check | High Level |  |

The properties below are categorized as valid state properties, which can be used to assume a valid storage state in other high-level properties. 

| Property | Description | Category | Mutation |
| --- | --- | --- | --- |
| ST-01 | Vault MUST NOT be deinitialized | Valid State | |
| ST-02 | Uninitialized snapshot MUST be reset | Valid State | |
| ST-03 | Snapshot stamp MUST be always equal to 1 | Valid State | |
| ST-04 | Last interest accumulator timestamp set when positive accumulated fees | Valid State | |
| ST-05 | Last interest accumulator timestamp MUST NOT be in the future | Valid State | |
| ST-06 | Cash amount MUST NOT be less than the ERC20 assets stored in the current contract | Valid State | [Vault/Vault_0.sol](./mutations/Vault/Vault_0.sol) |
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
| ST-25 | Transfer assets to zero address not allowed | Valid State | [AssetTransfers/AssetTransfers_0.sol](./mutations/AssetTransfers/AssetTransfers_0.sol) |
| ST-26 | Interest rate has a maximum limit of 1,000,000 APY | Valid State |  |
| ST-27 | User interest accumulator always less or equal vault interest accumulator | Valid State | |
| ST-28 | User's interest accumulator set when non-zero owed | Valid State |  |
| ST-29 | Interest accumulator is scaled by 1e27 | Valid State |  |
| ST-30 | Interest rate zero when interest rate model contract is not set| Valid State |  |
| ST-31 | Owner and spender in allowances should differ | Valid State |  |

## Vault

| Property | Description | Category | Mutation |
| --- | --- | --- | --- |
| VLT-01 | Accumulated fees MUST always be less than or equal to total shares | Valid State |  |
| VLT-02 | User balance plus accumulated fees MUST always be equal to the total shares (with only 1 user) | Valid State |  |
| VLT-03 | Sum of three users' balance MUST always be equal to the total shares (with only 3 users) | Valid State |  |
| VLT-04 | The vault's cash changes MUST be accompanied by assets transfer (when no surplus assets available) | High Level |  |
| VLT-05 | Changes in the cash balance MUST correspond to changes in user's shares | High Level |  |
| VLT-06 | Snapshot is disabled if both caps are disabled (at low-level set to 0, but resolved to max_uint256) | Valid State |  |
| VLT-07 | View functions don't update the state | State Transition |  |
| VLT-08 | State change functions are protected against reentrancy | Valid State |  |
| VLT-09 | Anyone can execute view functions | State Transition |  |
| VLT-10 | Specific view functions are protected against reentrancy, while others are not | Valid State |  |
| VLT-11 | Specific functions can modify state | State Transition |  |
| VLT-12 | Possibility of modifying state | State Transition |  |
| VLT-13 | Hook execution allowance | Valid State |  |
| VLT-14 | Hook execution possibility | State Transition |  |
| VLT-15 | Hook execution restriction | Valid State |  |

## Governance

| Property | Description | Category | Mutation |
| --- | --- | --- | --- |
| GOV-01 | Only the governor can invoke methods that modify the configuration of the vault | High Level |  |
| GOV-02 | Only one governor can exist at one time | Valid State |  |
| GOV-03 | Governor's ownership can be transferred | Unit Test |  |
| GOV-04 | The ownership could be revoked by setting the governor to zero address | Unit Test |  |
| GOV-05 | The fee receiver address can be changed | Unit Test |  |
| GOV-06 | While distributing fees, external protocol config contract is used | State Transition | [Governance/1.sol](./mutations/Governance/1.sol) |
| GOV-07 | View functions MUST NOT be protected against reentrancy | Valid State | [Governance/5.sol](./mutations/Governance/5.sol) |
| GOV-08 | View functions don't update state | State Transition |  |
| GOV-09 | The governor fee receiver can be disabled | Unit Test |  |
| GOV-10 | If the governor receiver was not set, the protocol gets all fees | High Level |  |
| GOV-11 | Protocol's fee share cannot be more than the max protocol fee share (50%) | High Level |  |
| GOV-12 | While distributing fees, total shares MUST NOT change and accumulated fees are cleared | State Transition |  |
| GOV-13 | While distributing fees, shares are transferred to governor and protocol fee receiver addresses | State Transition |  |
| GOV-14 | Non-governor methods MUST be accessible to any callers | Valid State |  |
| GOV-15 | The LTV can be set for a collateral asset, including borrow LTV, liquidation LTV, and ramp duration | Unit Test |  |
| GOV-16 | LTV can be increased or decreased immediately | State Transition |  |
| GOV-17 | Initial liquidation LTV is always the previous liquidation LTV or greater than liquidation LTV when ramping | Valid State |  |
| GOV-18 | Specific functions can modify state | State Transition | [Governance/2.sol](./mutations/Governance/2.sol) |
| GOV-19 | Possibility of modifying state | State Transition |  |
| GOV-20 | State change functions are protected against reentrancy | Valid State | [Governance/3.sol](./mutations/Governance/3.sol) |
| GOV-21 | Anyone can execute view functions | Valid State | [Governance/6.sol](./mutations/Governance/6.sol) |
| GOV-22 | Hook execution allowance | Valid State |  |
| GOV-23 | Hook execution possibility | State Transition |  |
| GOV-24 | Hook execution restriction | Valid State |  |

## RiskManager

| Property | Description | Category | Mutation |
| --- | --- | --- | --- |
| RM-01 | Total shares and total borrows limitations | Valid State | |
| RM-02 | View functions don't update the state | State Transition |  |
| RM-03 | Specific functions can modify state | State Transition |  |
| RM-04 | Possibility of modifying state | State Transition |  |
| RM-05 | Specific view functions are protected against reentrancy | Valid State |  |
| RM-06 | Hook execution restriction | Valid State |  |

## Liquidation

| Property | Description | Category | Mutation |
| --- | --- | --- | --- |
| LIQ-01 | Liquidation operations are prohibited until the cool-down period has passed | High Level |  |
| LIQ-02 | Check liquidation healthy | High Level |  |
| LIQ-03 | View functions don't update the state | State Transition |  |
| LIQ-04 | State change functions are protected against reentrancy | Valid State |  |
| LIQ-05 | Specific functions can modify state | State Transition |  |
| LIQ-06 | Possibility of modifying state | State Transition |  |
| LIQ-07 | Specific view functions are protected against reentrancy | Valid State |  |
| LIQ-08 | Possibility of liquidation | High Level |  |
| LIQ-09 | Hook execution allowance | Valid State |  |
| LIQ-10 | Hook execution possibility | State Transition |  |
| LIQ-11 | Hook execution restriction | Valid State |  |

## Borrowing

| Property | Description | Category | Mutation |
| --- | --- | --- | --- |
| BRW-01 | View functions don't update the state | State Transition |  |
| BRW-02 | State change functions are protected against reentrancy | Valid State |  |
| BRW-03 | Specific functions can modify state | State Transition |  |
| BRW-04 | Possibility of modifying state | State Transition |  |
| BRW-05 | Specific view functions are protected against reentrancy | Valid State |  |
| BRW-06 | Hook execution allowance | Valid State |  |
| BRW-07 | Hook execution possibility | State Transition |  |
| BRW-08 | Hook execution restriction | Valid State |  |

## Violated

List of violated properties.

| Property | Description | Category | Fix |
| --- | --- | --- | --- |
| L1 | protocolFeeShare() displays icorrect value as it doesn't consider 50% limit | Unit Test | [Governance_L1_fix/1.sol](./mutations/Governance_L1_fix/1.sol) |
| L1-EX | Ensure that protocol fee receiver gets an amount of shares equal to what `protocolFeeShare()` getter returns | High Level | [Governance_L1_fix/1.sol](./mutations/Governance_L1_fix/1.sol) |
