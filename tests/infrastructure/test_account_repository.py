import pytest 
from ledger.infrastructure.repositories.account_repository import AccountRepository
from ledger.infrastructure.repositories.transaction_repository import TransactionRepository
from ledger.domain.account import Account, AccountType
from ledger.domain.transaction import Transaction
import uuid
from ledger.domain.entry import LedgerEntry 
from decimal import Decimal


def test_create_fetch_account(session):
    account_repo = AccountRepository(session)
    account = Account(name='Test Account', account_type=AccountType.ASSET)

    account_repo.create(account)

    fetched = account_repo.get_by_id(account.id)
    assert fetched is not None
    assert fetched.name == "Test Account"
    assert fetched.account_type == AccountType.ASSET


def test_list_all_account(session):
    account_repo = AccountRepository(session)
    account1 = Account(name='Account 1', account_type=AccountType.ASSET)
    account2 = Account(name='Account 2', account_type=AccountType.REVENUE)

    account_repo.create(account1)
    account_repo.create(account2)

    accounts = account_repo.list_all()

    assert len(accounts) == 2
    assert {account.id for account in accounts} == {account1.id, account2.id}
    assert {account.name for account in accounts} == {'Account 1', 'Account 2'}

def test_account_get_balance(session):
    account_repo = AccountRepository(session)
    txn_repo = TransactionRepository(session)

    wallet = Account(name="Test Wallet", account_type=AccountType.ASSET)
    revenue = Account(name="Test Revenue", account_type=AccountType.REVENUE)
    account_repo.create(wallet)
    account_repo.create(revenue)

    entries = [
        LedgerEntry(account=wallet, amount=Decimal("100"), is_debit=True),
        LedgerEntry(account=revenue, amount=Decimal("100"), is_debit=False),
    ]
    transaction = Transaction(description="Test transfer", ledger_entries=entries)
    txn_repo.create(transaction)
    session.commit()

    assert account_repo.get_balance(account_id=wallet.id) == Decimal("-100")
    assert account_repo.get_balance(account_id=revenue.id) == Decimal("100")

def test_get_balance_returns_zero_for_empty_account(session):
    account_repo = AccountRepository(session)
    account = Account(name="Empty Account", account_type=AccountType.ASSET)
    account_repo.create(account)

    assert account_repo.get_balance(account_id=account.id) == Decimal("0")
