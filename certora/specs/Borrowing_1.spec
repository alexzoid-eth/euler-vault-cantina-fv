import "./base/Borrowing.spec";
import "./ValidState.spec";

// @todo BRW- | Snapshot total borrow assets MUST set from storage total borrow shares, rounding up
rule snapshotTotalBorrowAssetsSetFromStorage(env e, method f, calldataarg args) 
    filtered { f -> !HARNESS_METHODS(f) } {

    requireInvariant uninitializedSnapshotReset;
    requireInvariant snapshotDisabledWithBothCapsDisabled;

    bool initialized = ghostSnapshotInitialized;
    mathint totalBorrowsPrev = totalBorrowsExact(e);

    f(e, args);

    // Total borrows in snapshot was changed
    assert(ghostSnapshotInitialized && initialized != ghostSnapshotInitialized
        => (totalBorrowsExact(e) == totalBorrowsPrev
            // Total borrows in storage was NOT changed in this transaction
            => ghostSnapshotBorrows == totalBorrows(e))
            )
    );
}
