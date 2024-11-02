from abc import ABC, abstractmethod

class BankAccount(ABC):
    def __init__(self, account_number, owner, balance=0.0):
        self.account_number = account_number
        self.owner = owner
        self.balance = balance
        self.is_active = True

    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def transfer(self, target_account, amount):
        pass

    @abstractmethod
    def apply_monthly_changes(self):
        pass

    def get_account_info(self):
        return {
            "account_number": self.account_number,
            "owner": self.owner,
            "balance": self.balance,
            "is_active": self.is_active,
            "account_type": self.__class__.__name__
        }

    def get_balance_report(self):
        return f"Balance for {self.owner}'s {self.__class__.__name__}: {self.balance}"

    def activate_account(self):
        self.is_active = True

    def deactivate_account(self):
        self.is_active = False


class PayrollAccount(BankAccount):
    def withdraw(self, amount):
        if not self.is_active:
            print("Account is inactive.")
            return False
        if amount > self.balance:
            print("Insufficient balance.")
            return False
        self.balance -= amount
        return True

    def deposit(self, amount):
        raise NotImplementedError("Deposits are not allowed for Payroll Accounts.")

    def transfer(self, target_account, amount):
        raise NotImplementedError("Transfers are not allowed from Payroll Accounts.")

    def apply_monthly_changes(self):
        pass  # No monthly changes for payroll accounts


class DebitAccount(BankAccount):
    def __init__(self, account_number, owner, balance=0.0, interest_rate=0.01, required_balance=100.0):
        super().__init__(account_number, owner, balance)
        self.interest_rate = interest_rate
        self.required_balance = required_balance

    def withdraw(self, amount):
        if not self.is_active:
            print("Account is inactive.")
            return False
        if amount > self.balance:
            print("Insufficient balance.")
            return False
        self.balance -= amount
        return True

    def deposit(self, amount):
        if not self.is_active:
            print("Account is inactive.")
            return False
        self.balance += amount
        return True

    def transfer(self, target_account, amount):
        if not self.is_active:
            print("Account is inactive.")
            return False
        if amount > self.balance:
            print("Insufficient balance.")
            return False
        self.balance -= amount
        target_account.balance += amount
        return True

    def apply_monthly_changes(self):
        if self.is_active:
            self.balance *= (1 + self.interest_rate)  # Apply compound interest
            if self.balance < self.required_balance:
                self.deactivate_account()


class CreditAccount(BankAccount):
    def __init__(self, account_number, owner, balance=0.0, credit_limit=500.0, interest_rate=0.02):
        super().__init__(account_number, owner, balance)
        self.credit_limit = credit_limit
        self.credit_balance = 0.0  # The amount owed
        self.interest_rate = interest_rate

    def withdraw(self, amount):
        if not self.is_active:
            print("Account is inactive.")
            return False
        if self.credit_balance + amount > self.credit_limit:
            print("Credit limit exceeded.")
            return False
        self.credit_balance += amount
        return True

    def deposit(self, amount):
        if not self.is_active:
            print("Account is inactive.")
            return False
        self.credit_balance = max(0, self.credit_balance - amount)
        return True

    def transfer(self, target_account, amount):
        if not self.is_active:
            print("Account is inactive.")
            return False
        if self.credit_balance + amount > self.credit_limit:
            print("Credit limit exceeded.")
            return False
        self.credit_balance += amount
        target_account.balance += amount
        return True

    def apply_monthly_changes(self):
        if self.is_active and self.credit_balance > 0:
            self.credit_balance *= (1 + self.interest_rate)  # Apply interest to credit owed


class BankSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_type, owner, initial_balance=0.0):
        account_number = f"ACC{len(self.accounts) + 1:04}"
        if account_type == 'payroll':
            account = PayrollAccount(account_number, owner, initial_balance)
        elif account_type == 'debit':
            account = DebitAccount(account_number, owner, initial_balance)
        elif account_type == 'credit':
            account = CreditAccount(account_number, owner, initial_balance)
        else:
            raise ValueError("Invalid account type.")
        
        self.accounts[account_number] = account
        return account

    def transfer_funds(self, from_account, to_account, amount):
        if from_account not in self.accounts or to_account not in self.accounts:
            print("One or both accounts do not exist.")
            return False
        return self.accounts[from_account].transfer(self.accounts[to_account], amount)

    def monthly_update(self):
        for account in self.accounts.values():
            account.apply_monthly_changes()

    def deactivate_account(self, account_number):
        if account_number in self.accounts:
            self.accounts[account_number].deactivate_account()

    def activate_account(self, account_number):
        if account_number in self.accounts:
            self.accounts[account_number].activate_account()

    def get_account_info(self, account_number):
        if account_number in self.accounts:
            return self.accounts[account_number].get_account_info()
        return "Account not found."

    def get_balance_report(self, account_number):
        if account_number in self.accounts:
            return self.accounts[account_number].get_balance_report()
        return "Account not found."