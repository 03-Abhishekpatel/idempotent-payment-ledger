from sqlalchemy.orm import Session
from ledger.domain.transaction import Transaction
from ledger.infrastructure.db.mappers import transaction_to_model, transaction_to_domain
import uuid
from ledger.infrastructure.db.models import TransactionModel

class TransactionRepository:
    def __init__(self, session: Session):
        self.session = session 

    def create(self, transaction: Transaction) -> Transaction:
        transaction_model = transaction_to_model(transaction)

        self.session.add(transaction_model)
        self.session.flush()

        return transaction_to_domain(transaction_model)

    def get_by_id(self, transaction_id: uuid.UUID) -> Transaction:
        model = self.session.get(TransactionModel, transaction_id)
        return transaction_to_domain(model) if model else None


    