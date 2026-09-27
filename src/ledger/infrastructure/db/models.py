from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, Numeric, DateTime, func, CheckConstraint, UUID, BOOLEAN, TEXT, ForeignKey
import uuid 
from ledger.domain.account import AccountType
from decimal import Decimal
from datetime import datetime 


class AccountModel(Base):
    __tablename__ = 'account'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255))
    account_type: Mapped[AccountType] = mapped_column( Enum(AccountType, name="account_type_enum"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ledger_entries: Mapped[list["LedgerEntryModel"]] = relationship(back_populates="account")


class LedgerEntryModel(Base):
    __tablename__ = "ledger_entry"
    __table_args__ = (
        CheckConstraint("amount > 0", name="ck_amount_positive"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 2))
    account_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('account.id'), index=True)
    transaction_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('transaction.id'), index=True)
    is_debit: Mapped[bool] = mapped_column(BOOLEAN)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    transaction: Mapped["TransactionModel"] = relationship(back_populates="ledger_entries")
    account: Mapped["AccountModel"] = relationship(back_populates="ledger_entries")


class TransactionModel(Base):
    __tablename__ = "transaction"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    description: Mapped[str] = mapped_column(TEXT)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ledger_entries: Mapped[list["LedgerEntryModel"]] = relationship(back_populates="transaction")

    