#!/bin/bash

PARAMS="$@"

certora/mutations/checkMutation.sh Borrowing_ValidState $PARAMS
certora/mutations/checkMutation.sh Governance_ValidState $PARAMS
certora/mutations/checkMutation.sh Liquidation_ValidState $PARAMS
certora/mutations/checkMutation.sh RiskManager_ValidState $PARAMS
certora/mutations/checkMutation.sh Vault_ValidState $PARAMS
