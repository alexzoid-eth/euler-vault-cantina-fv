using ProtocolConfig as _ProtocolConfig;

//
// Ghost copy of minInterestFee
//

ghost mathint ghostProtocolConfigMinInterestFee {
    init_state axiom ghostProtocolConfigMinInterestFee == 0;
    axiom ghostProtocolConfigMinInterestFee >= 0 && ghostProtocolConfigMinInterestFee <= max_uint16;
}

hook Sload uint16 val _ProtocolConfig.minInterestFee {
    require(require_uint16(ghostProtocolConfigMinInterestFee) == val);
}

hook Sstore _ProtocolConfig.minInterestFee uint16 val {
    ghostProtocolConfigMinInterestFee = val;
}

//
// Ghost copy of maxInterestFee
//

ghost mathint ghostProtocolConfigMaxInterestFee {
    init_state axiom ghostProtocolConfigMaxInterestFee == 0;
    axiom ghostProtocolConfigMaxInterestFee >= 0 && ghostProtocolConfigMaxInterestFee <= max_uint16;
}

hook Sload uint16 val _ProtocolConfig.maxInterestFee {
    require(require_uint16(ghostProtocolConfigMaxInterestFee) == val);
}

hook Sstore _ProtocolConfig.maxInterestFee uint16 val {
    ghostProtocolConfigMaxInterestFee = val;
}

//
// Ghost copy of _interestFeeRanges[].exists
//

ghost mapping (address => bool) ghostProtocolConfigRangeExists {
    init_state axiom forall address i. ghostProtocolConfigRangeExists[i] == false;
}

hook Sload bool val _ProtocolConfig._interestFeeRanges[KEY address i].exists {
    require(ghostProtocolConfigRangeExists == val);
} 

hook Sstore _ProtocolConfig._interestFeeRanges[KEY address i].exists bool val {
    ghostProtocolConfigRangeExists[i] = val;
}
