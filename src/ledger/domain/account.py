import uuid
from enum import Enum
class AccountType(str, Enum):
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"
    EQUITY = "EQUITY"
    REVENUE = "REVENUE"
    EXPENSE = "EXPENSE"


class Account:

    def __init__(self, name: str, account_type: AccountType, account_id: uuid.UUID | None = None):
        if not name or not name.strip():
            raise ValueError("Account name must not be empty")
        
        if not isinstance(account_type, AccountType):
            raise TypeError(f"account_type must be an AccountType, got {type(account_type)!r}")    

        if account_id and not isinstance(account_id, uuid.UUID):
            raise TypeError(f"account_id must be an uuid type, get {type(account_id)!r}")
        
        self.id = account_id or uuid.uuid4() 
        self.name = name 
        self.account_type = account_type

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Account) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return (
            f"Account(id={self.id}, name={self.name}, account_type={self.account_type})"
        )