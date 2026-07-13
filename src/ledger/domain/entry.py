from decimal import Decimal
from datetime import datetime, UTC


class LedgerEntry:
    def __init__(self, account, amount: Decimal, is_debit: bool, transaction_id):
        self.account = account
        self.amount = amount
        self.is_debit = is_debit
        self.transaction_id = transaction_id

    

    

    
