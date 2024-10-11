import unittest
from app import Account, accounts  # Import the Account class and the global accounts dictionary

class TestBankOperations(unittest.TestCase):
    def setUp(self):
        # Create two accounts for testing
        self.account1 = Account(1000)  # Initial balance: 1000
        self.account2 = Account(500)   # Initial balance: 500

        # Add the accounts to the global accounts dictionary using their account numbers
        accounts[self.account1.account_number] = self.account1
        accounts[self.account2.account_number] = self.account2

    def test_create_account(self):
        """Test creating a new account with an initial balance."""
        new_account = Account(300)
        self.assertEqual(new_account.balance, 300)

    def test_deposit_valid_amount(self):
        """Test depositing a valid amount."""
        message = self.account1.deposit(200)
        self.assertEqual(self.account1.balance, 1200)
        self.assertEqual(message, "Deposit successful. New balance: $1200.00")

    def test_deposit_negative_amount(self):
        """Test depositing a negative amount (invalid)."""
        message = self.account1.deposit(-50)
        self.assertEqual(message, "Invalid amount. Deposit cannot be negative.")

    def test_withdraw_valid_amount(self):
        """Test withdrawing a valid amount."""
        message = self.account1.withdraw(300)
        self.assertEqual(self.account1.balance, 700)
        self.assertEqual(message, "Withdrawal successful. New balance: $700.00")

    def test_withdraw_exceeding_balance(self):
        """Test withdrawing an amount that exceeds the balance."""
        message = self.account1.withdraw(1500)
        self.assertEqual(message, "Insufficient funds. Withdrawal denied.")
        self.assertEqual(self.account1.balance, 1000)

    def test_transfer_valid_amount(self):
        """Test transferring a valid amount between accounts."""
        message = self.account1.transfer(self.account2.account_number, 400)
        self.assertEqual(self.account1.balance, 600)
        self.assertEqual(self.account2.balance, 900)
        self.assertEqual(message, "Transfer successful. $400.00 was transferred.")

    def test_transfer_exceeding_balance(self):
        """Test transferring an amount that exceeds the balance."""
        message = self.account1.transfer(self.account2.account_number, 2000)
        self.assertEqual(message, "Transfer failed. Unable to withdraw the full amount.")
        self.assertEqual(self.account1.balance, 1000)
        self.assertEqual(self.account2.balance, 500)

    def test_transfer_to_nonexistent_account(self):
        """Test transferring to an account number that does not exist."""
        message = self.account1.transfer("9999999999", 100)
        self.assertEqual(message, "Transfer failed. Recipient account not found.")
        self.assertEqual(self.account1.balance, 1000)

    def test_transfer_to_same_account(self):
        """Test transferring to the same account (should raise error)."""
        message = self.account1.transfer(self.account1.account_number, 100)
        self.assertEqual(message, "Transfer failed. Unable to withdraw the full amount.")
        self.assertEqual(self.account1.balance, 1000)

if __name__ == '__main__':
    unittest.main()
