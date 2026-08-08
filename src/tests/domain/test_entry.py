from ledger.domain.entry import LedgerEntry
from ledger.domain.account import Account, AccountType
import pytest  
from decimal import Decimal 
from ledger.domain.exceptions import InvalidAmountError
import dataclasses
import uuid

# @pytest.fixture
# def account():
#     return Account("Test Account", AccountType.ASSET)

def test_valid_entry_construct():
    account = Account("Test Account", AccountType.ASSET)
    entry = LedgerEntry(account = account, amount = Decimal("100"), is_debit = True)

    assert isinstance(entry, LedgerEntry)
    assert entry.amount == Decimal("100")
    assert entry.is_debit is True 

def test_debit_signed_amount_is_negative():
    account = Account("Test Account", AccountType.ASSET)
    entry = LedgerEntry(account = account, amount = Decimal("200"), is_debit = True)
    sign_amount = entry.signed_amount() 

    assert sign_amount == Decimal("-200")

def test_credit_signed_amount_is_positive():
    account = Account("Test Account", AccountType.ASSET)
    entry = LedgerEntry(account = account, amount = Decimal("100"), is_debit = False)
    sign_amount = entry.signed_amount()

    assert sign_amount == Decimal("100")

def test_zero_or_negative_amount_raise_error():
    account = Account("Test Account", AccountType.ASSET)

    with pytest.raises(InvalidAmountError):
        LedgerEntry(account = account, amount = Decimal("0"), is_debit = True)

    with pytest.raises(InvalidAmountError):
        LedgerEntry(account = account, amount = Decimal("-200"), is_debit = True)

def test_float_amount_raise_error():
    account = Account("Test Account", AccountType.ASSET)

    with pytest.raises(TypeError):
        LedgerEntry(account = account, amount = 50.0, is_debit = True)

def test_entry_is_frozen():
    account = Account("Test Account", AccountType.ASSET)

    entry = LedgerEntry(account = account, amount = Decimal("200"), is_debit = True)

    with pytest.raises(dataclasses.FrozenInstanceError):
        entry.amount = Decimal("100")

    with pytest.raises(dataclasses.FrozenInstanceError):
        entry.is_debit = False

    with pytest.raises(dataclasses.FrozenInstanceError):
            entry.account = Account("Test Demo Account", AccountType.ASSET)

def test_entry_bounded_to_transaction():
    account = Account("Test Account", AccountType.ASSET)
    entry = LedgerEntry(account = account, amount = Decimal("200"), is_debit = True)

    new_transaction_id = uuid.uuid4() 
    bound = entry.bound_to_transaction(new_transaction_id)

    assert entry.transaction_id is None
    assert bound.transaction_id == new_transaction_id
    assert bound.id == entry.id