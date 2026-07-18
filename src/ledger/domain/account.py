class Account:
    def __init__(self, account_id: str, balance: float):
        self.account_id = account_id
        self.balance = balance 
        self.account_type = None
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError('Amount must be a positive')
        self.balance += amount 
        return True 
    
    def credit(self, withdraw_amount):
        if withdraw_amount < self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= withdraw_amount 
        return True
    