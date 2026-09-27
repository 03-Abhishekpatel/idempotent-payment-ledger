from ledger.domain.transaction import Transaction
from ledger.domain.entry import LedgerEntry 
from ledger.domain.account import AccountType, Account
from decimal import Decimal 
import pytest 
from ledger.domain.exceptions import UnbalancedTransactionError, InsufficientEntriesError


def test_balanced_transaction_constructs():
    account1 = Account("Alice Wallet", AccountType.ASSET)
    account2 = Account("Platform Revenue", AccountType.REVENUE)

    entry = [
        LedgerEntry(account = account1, amount=Decimal("100"), is_debit=True), 
        LedgerEntry(account = account2, amount=Decimal("100"), is_debit=False)
    ]

    transaction = Transaction(entry, "Transfer")

    assert len(transaction.ledger_entries) == 2
    for entry in transaction.ledger_entries:
        assert entry.transaction_id == transaction.id


def test_unbalanced_transaction_rejected():
    account1 = Account("Alice Wallet", AccountType.ASSET)
    account2 = Account("Platform Revenue", AccountType.REVENUE)

    entry = [
        LedgerEntry(account = account1, amount=Decimal("100"), is_debit=True), 
        LedgerEntry(account = account2, amount=Decimal("50"), is_debit=False)
    ]

    with pytest.raises(UnbalancedTransactionError):
        Transaction(entry, "Bad Withdrawl")

def test_single_entry_rejected():
    account1 = Account("Top Wallet", AccountType.ASSET)

    entry = [
        LedgerEntry(account = account1, amount = Decimal("100"), is_debit=True)
    ]

    with pytest.raises(InsufficientEntriesError):
        Transaction(entry, "Single Entry")

def test_decimal_precision_not_lost():
    account1 = Account("Top Wallet", AccountType.ASSET)
    account2 = Account("DOK Wallet", AccountType.ASSET)
    account3 = Account("Platform Revenue", AccountType.REVENUE)

    entry = [
        LedgerEntry(account = account1, amount = Decimal("0.1"), is_debit=True),
        LedgerEntry(account = account2, amount = Decimal("0.2"), is_debit=True),
        LedgerEntry(account = account3, amount = Decimal("0.3"), is_debit=False),
    ]

    transaction = Transaction(entry, "Verify Sum Precision through Split payment")

    assert transaction.ledger_entries[0].amount + transaction.ledger_entries[1].amount == transaction.ledger_entries[2].amount
    assert len(transaction.ledger_entries) == 3

def test_ledger_entry_is_immutable_tuple():
    account1 = Account("DOK Wallet", AccountType.ASSET)
    account2 = Account("Platform Revenue", AccountType.REVENUE)

    entry = [
        LedgerEntry(account = account1, amount=Decimal("100"), is_debit=True), 
        LedgerEntry(account = account2, amount=Decimal("100"), is_debit=False)
    ]

    transaction = Transaction(entry, "Shopping")
    assert isinstance(transaction.ledger_entries, tuple)




