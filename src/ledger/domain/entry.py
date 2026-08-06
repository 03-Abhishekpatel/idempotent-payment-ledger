from decimal import Decimal
from .account import Account
import uuid
from dataclasses import dataclass, field
from .exceptions import InvalidAmountError

@dataclass(frozen=True)
class LedgerEntry:
    account: Account
    amount: Decimal 
    is_debit: bool
    transaction_id: uuid.UUID | None = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self) -> None:
        if not isinstance(self.account, Account):
            raise TypeError(f"account must type of Account, get {type(self.account)!r}")

        if not isinstance(self.amount, Decimal):
            raise TypeError(f"amount must type of Decimal, get {type(self.amount)!r}")

        if self.amount <= Decimal("0"):
            raise InvalidAmountError(
                f"amount must be strictly positive; direction is carried by is_debit, got {self.amount}"
            )


    def signed_amount(self) -> Decimal:
        return -self.amount if self.is_debit else self.amount

    def bound_to_transaction(self, transaction_id: uuid.UUID) -> LedgerEntry:

        return LedgerEntry(
            account = self.account,
            amount = self.amount, 
            is_debit = self.is_debit, 
            transaction_id=transaction_id,
            id = self.id
        )
    