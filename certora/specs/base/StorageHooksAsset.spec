using DummyERC20A as _Asset;

//
// Ghost copy of balances
//

ghost mapping (address => mathint) ghostErc20Balances {
    init_state axiom forall address i. ghostErc20Balances[i] == 0;
    axiom forall address i. ghostErc20Balances[i] >= 0 && ghostErc20Balances[i] <= max_uint256;
}

hook Sload uint256 val _Asset.b[KEY address i] {
    require(require_uint256(ghostErc20Balances[i]) == val);
} 

hook Sstore _Asset.b[KEY address i] uint256 val {
    ghostErc20Balances[i] = val;
}

//
// Ghost copy of allowances
//

ghost mapping(address => mapping(address => mathint)) ghostErc20Allowances {
    init_state axiom forall address key. forall address val. ghostErc20Allowances[key][val] == 0;
    axiom forall address key. forall address val. ghostErc20Allowances[key][val] >= 0 && ghostErc20Allowances[key][val] <= max_uint256;
}

hook Sload uint256 amount _Asset.a[KEY address key][KEY address val] {
    require(require_uint256(ghostErc20Allowances[key][val]) == amount);
}

hook Sstore _Asset.a[KEY address key][KEY address val] uint256 amount {
    ghostErc20Allowances[key][val] = amount;
}

//
// Ghost copy of totalSupply
//

ghost mathint ghostErc20TotalSupply {
    init_state axiom ghostErc20TotalSupply == 0;
    axiom ghostErc20TotalSupply >= 0 && ghostErc20TotalSupply <= max_uint256;
}

hook Sload uint256 val _Asset.t {
    require(require_uint256(ghostErc20TotalSupply) == val);
}

hook Sstore _Asset.t uint256 val {
    ghostErc20TotalSupply = val;
}
