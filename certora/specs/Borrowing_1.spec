import "./base/Borrowing.spec";
import "./common/State.spec";

// @todo (mutation) BR1-01 | Sum of three users' borrows must always be equal to the total borrows

function sumOfUsersBorrowsEqualTotalBorrowsReqCVL(address user1, address user2, address user3) {
    // Data of any other addresses are zero
    require(forall address u. u != user1 && u != user2 && u != user3 => ghostUsersData[u] == 0);
    // All users are different and not zero
    require(user1 != user2 && user1 != user3 && user2 != user3);
    require(user1 != 0 && user2 != 0 && user3 != 0);
}

invariant sumOfUsersBorrowsEqualTotalBorrows(env e, address user1, address user2, address user3) 
    debtOfExactHarness(e, user1) + debtOfExactHarness(e, user2) + debtOfExactHarness(e, user3) == ghostTotalBorrows {
    preserved {
        sumOfUsersBorrowsEqualTotalBorrowsReqCVL(user1, user2, user3);
    }
}