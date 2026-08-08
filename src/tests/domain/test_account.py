from ledger.domain.account import Account, AccountType
import uuid
import pytest

def test_account_with_valid_data():
    acc = Account("Dok Wallet", AccountType.ASSET)
    assert isinstance(acc, Account)
    assert acc.name == "Dok Wallet"
    assert acc.account_type == AccountType.ASSET


def  test_empty_name_raise_error():
    with pytest.raises(ValueError):
        Account("", AccountType.ASSET)

def test_whitespace_only_name_rejected():
    with pytest.raises(ValueError):
        Account("     ", AccountType.ASSET)

def test_invalid_account_type():
    with pytest.raises(TypeError):
        Account("Dok Wallet", "ASSET")

def test_two_account_have_distinct_ids():
    acc1 = Account("Dok  Wallet", AccountType.ASSET)
    acc2 = Account("Top Wallet", AccountType.ASSET)

    assert acc1.id != acc2.id 

def test_account_have_given_ids():
    acc_id = uuid.uuid4()
    acc = Account("Test Wallet", AccountType.ASSET, acc_id)
    
    assert acc.id == acc_id
