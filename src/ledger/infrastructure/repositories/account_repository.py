from ledger.domain.account import Account
from sqlalchemy.orm import Session
from ledger.infrastructure.db.mappers import account_to_domain, account_to_model
from ledger.infrastructure.db.models import AccountModel,LedgerEntryModel
from uuid import UUID
from decimal import Decimal
from sqlalchemy import func, case, select

class AccountRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, account: Account) -> Account:

        model = account_to_model(account)
        self.session.add(model)
        self.session.flush() 
        return account_to_domain(model)

    def get_by_id(self, id: UUID) -> Account:

        model = self.session.get(AccountModel, id)
        return account_to_domain(model) if model else None 

    def list_all(self) -> list[Account]:
        models = self.session.query(AccountModel).all() 
        return [account_to_domain(m) for m in models]

    def get_balance(self, account_id: UUID) -> Decimal:
        stmt = select(
            func.coalesce(
                func.sum(
                    case(   
                        (LedgerEntryModel.is_debit.is_(True), -LedgerEntryModel.amount),
                        else_=LedgerEntryModel.amount,
                    )
                ),
                0,
            )
        ).where(LedgerEntryModel.account_id == account_id)
        result = self.session.execute(stmt).scalar_one()
        return Decimal(result)

    