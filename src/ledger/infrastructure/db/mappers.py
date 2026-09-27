from ledger.infrastructure.db.models import AccountModel, TransactionModel, LedgerEntryModel
from ledger.domain.account import Account, AccountType
from ledger.domain.entry import LedgerEntry
from ledger.domain.transaction import Transaction

def account_to_model(account: Account) -> AccountModel:
    account_model = AccountModel(
        id = account.id, 
        name = account.name, 
        account_type = account.account_type 
    )

    return account_model

def account_to_domain(account_model: AccountModel) -> Account:
    account_type = account_model.account_type
    if isinstance(account_type, str):
        account_type = AccountType(account_type)
    elif not isinstance(account_type, AccountType):
        account_type = AccountType(account_type)

    account = Account(
        id = account_model.id,
        name = account_model.name,
        account_type = account_type,
    )

    return account

def transaction_to_domain(transaction_model: TransactionModel) -> Transaction:
    entries = [ledger_entry_to_domain(e) for e in transaction_model.ledger_entries]

    transaction = Transaction(
        id = transaction_model.id, 
        timestamp = transaction_model.timestamp, 
        description = transaction_model.description, 
        ledger_entries = entries
    )

    return transaction


def transaction_to_model(transaction: Transaction) -> TransactionModel:
    model_entries = [ledger_entry_to_model(e) for e in transaction.ledger_entries]
    transaction_model = TransactionModel(
        id = transaction.id,
        timestamp = transaction.timestamp, 
        description = transaction.description,
        ledger_entries = model_entries
    )

    return transaction_model

def ledger_entry_to_model(ledger_entry: LedgerEntry) -> LedgerEntryModel:
    model = LedgerEntryModel(
        id = ledger_entry.id,
        account_id = ledger_entry.account.id,
        amount = ledger_entry.amount,
        transaction_id = ledger_entry.transaction_id,
        is_debit = ledger_entry.is_debit,
    )

    return model

def ledger_entry_to_domain(model: LedgerEntryModel) -> LedgerEntry:
    domain = LedgerEntry(
        id = model.id,
        account = account_to_domain(model.account), 
        amount = model.amount,
        is_debit = model.is_debit,
        transaction_id = model.transaction_id,
    )

    return domain


