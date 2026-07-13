from datetime import datetime, UTC
from entry import LedgerEntry 

class Transaction:
    def __init__(self, transaction_id, timestamp: datetime, description: str, ledger_entries: list[LedgerEntry]):
        self.transaction_id = transaction_id
        self.timestamp = timestamp.datetime.now(UTC)
        self.description = description 
        self.ledger_entries = ledger_entries
    
    
    
