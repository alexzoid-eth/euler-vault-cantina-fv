#!/bin/bash

PARAMS="$@"

certora/scripts/check_mutation.sh Borrowing_Common $PARAMS
certora/scripts/check_mutation.sh Governance_Common $PARAMS
certora/scripts/check_mutation.sh Liquidation_Common $PARAMS
certora/scripts/check_mutation.sh RiskManager_Common $PARAMS
certora/scripts/check_mutation.sh Vault_Common $PARAMS
