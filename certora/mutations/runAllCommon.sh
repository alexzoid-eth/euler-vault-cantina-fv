#!/bin/bash

PARAMS="$@"

certora/mutations/checkMutation.sh Borrowing_Common $PARAMS
certora/mutations/checkMutation.sh Governance_Common $PARAMS
certora/mutations/checkMutation.sh Liquidation_Common $PARAMS
certora/mutations/checkMutation.sh RiskManager_Common $PARAMS
certora/mutations/checkMutation.sh Vault_Common $PARAMS
