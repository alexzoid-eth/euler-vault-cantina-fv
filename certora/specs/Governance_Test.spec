rule test(env e) {

    storage init = lastStorage;

    convertFees(e) at init;
    storage after1 = lastStorage;

    convertFees(e) at init;
    storage after2 = lastStorage;

    assert(after1[currentContract] == after2[currentContract]);
}
