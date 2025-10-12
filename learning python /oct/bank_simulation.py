# A simple, text-based bank simulation

class BankAccount:
    """A class to represent a single bank account."""

    def __init__(self, account_number, owner_name, initial_balance=0.0):
        """Initializes a new BankAccount."""
        self.account_number = account_number
        self.owner_name = owner_name
        self.balance = float(initial_balance)
        print(f"✅ Account #{self.account_number} for {self.owner_name} created with balance: ${self.balance:.2f}")

    def deposit(self, amount):
        """Adds a specified amount to the account balance."""
        if amount > 0:
            self.balance += amount
            print(f"💰 Deposited ${amount:.2f}. New balance: ${self.balance:.2f}")
        else:
            print("❌ Deposit amount must be positive.")

    def withdraw(self, amount):
        """Withdraws a specified amount if funds are sufficient."""
        if amount <= 0:
            print("❌ Withdrawal amount must be positive.")
        elif amount > self.balance:
            print(f"🚫 Insufficient funds! You only have ${self.balance:.2f} available.")
        else:
            self.balance -= amount
            print(f"💸 Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}")

    def get_balance(self):
        """Returns the current account balance."""
        print(f"ℹ️ Account #{self.account_number} balance: ${self.balance:.2f}")
        return self.balance

def main():
    """Main function to run the bank simulation."""
    # Use a dictionary to store bank accounts, with account number as the key
    bank_accounts = {}
    next_account_number = 1001

    print("🏦 Welcome to the Simple Bank Simulator! 🏦")

    while True:
        print("\n" + "="*30)
        print("Please choose an option:")
        print("1. Create a new account")
        print("2. Deposit money")
        print("3. Withdraw money")
        print("4. Check account balance")
        print("5. Exit")
        print("="*30)

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            owner_name = input("Enter the account owner's name: ")
            try:
                initial_balance = float(input("Enter initial deposit amount: $"))
                if initial_balance < 0:
                    print("❌ Initial deposit cannot be negative.")
                    continue
                # Create and store the new account
                bank_accounts[next_account_number] = BankAccount(next_account_number, owner_name, initial_balance)
                next_account_number += 1
            except ValueError:
                print("❌ Invalid amount. Please enter a number.")

        elif choice == '2':
            try:
                acc_num = int(input("Enter your account number: "))
                if acc_num in bank_accounts:
                    amount = float(input("Enter amount to deposit: $"))
                    bank_accounts[acc_num].deposit(amount)
                else:
                    print("❌ Account not found.")
            except ValueError:
                print("❌ Invalid input. Please enter numbers only.")

        elif choice == '3':
            try:
                acc_num = int(input("Enter your account number: "))
                if acc_num in bank_accounts:
                    amount = float(input("Enter amount to withdraw: $"))
                    bank_accounts[acc_num].withdraw(amount)
                else:
                    print("❌ Account not found.")
            except ValueError:
                print("❌ Invalid input. Please enter numbers only.")

        elif choice == '4':
            try:
                acc_num = int(input("Enter your account number: "))
                if acc_num in bank_accounts:
                    bank_accounts[acc_num].get_balance()
                else:
                    print("❌ Account not found.")
            except ValueError:
                print("❌ Invalid account number. Please enter a number.")

        elif choice == '5':
            print("👋 Thank you for using the Simple Bank Simulator. Goodbye!")
            break

        else:
            print("🤔 Invalid choice. Please select an option from 1 to 5.")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()