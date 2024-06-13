import "./base/Borrowing.spec";
import "./Common.spec";

// @todo (mutation) [1] BRW- | Sum of three users' borrows must always be equal to the total borrows

function sumOfUsersBorrowsEqualTotalBorrowsReqCVL(address user1, address user2, address user3) {
    // Data of any other addresses are zero
    require(forall address u. u != user1 && u != user2 && u != user3 => ghostUsersData[u] == 0);
    // All users are different and not zero
    require(user1 != user2 && user1 != user3 && user2 != user3);
    require(user1 != 0 && user2 != 0 && user3 != 0);
}

invariant sumOfUsersBorrowsEqualTotalBorrows(address user1, address user2, address user3) 
    OWED_FROM_DATA(ghostUsersData[user1]) + OWED_FROM_DATA(ghostUsersData[user2]) + OWED_FROM_DATA(ghostUsersData[user3]) 
        == ghostTotalBorrows {
    preserved {
        sumOfUsersBorrowsEqualTotalBorrowsReqCVL(user1, user2, user3);
    }
}

// BRW- | Accumulated fees must result in an increase in the total shares of the vault
rule accumulatedFeesIncreaseTotalShares(env e) {

    mathint accumulatedFeesPrev = ghostAccumulatedFees;
    mathint totalSharesPrev = ghostTotalShares;

    touch(e);
    
    assert(ghostAccumulatedFees >= accumulatedFeesPrev 
        => (ghostTotalShares - totalSharesPrev == ghostAccumulatedFees - accumulatedFeesPrev)
    );
}
