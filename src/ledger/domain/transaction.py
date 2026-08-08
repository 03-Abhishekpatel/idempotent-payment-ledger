from datetime import datetime, UTC
from .entry import LedgerEntry 
import uuid
from .exceptions import InsufficientEntriesError, UnbalancedTransactionError
from decimal import Decimal


MIN_ENTRIES = 2
ZERO = Decimal("0")

class Transaction:
    def __init__(self,
                ledger_entries: list[LedgerEntry],
                description: str,
                transaction_id: uuid.UUID | None = None,
                timestamp: datetime | None = None
            ):

        if len(ledger_entries) < MIN_ENTRIES:
            raise InsufficientEntriesError(
                f"Transaction requires at least {MIN_ENTRIES}, got {len(ledger_entries)}"
            )
        total = ZERO

        for entry in ledger_entries:
            total += entry.signed_amount()

        if total != ZERO:
            raise UnbalancedTransactionError(f"Transaction ledger entry sum to {total}, expected 0")
        

        self.id = transaction_id or uuid.uuid4()
        self.timestamp = timestamp or datetime.now(UTC)
        self.description = description 
        self.ledger_entries = tuple(entry.bound_to_transaction(self.id) for entry in ledger_entries) 

    def __repr__(self) -> str:
        return (
            f"Transaction(id={self.id}, description={self.description}), "
            f"entries={len(self.ledger_entries)}"
        )
