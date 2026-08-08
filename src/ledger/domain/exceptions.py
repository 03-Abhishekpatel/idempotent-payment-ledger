class LedgerDomainError(Exception):
    '''Base class for all Ledger Domain Error'''

class InvalidAmountError(LedgerDomainError):
    '''Raise when the amount is negative or zero in Leger Entry'''

class InsufficientEntriesError(LedgerDomainError):
    '''Raise when transaction have less than two ledger entries'''

class UnbalancedTransactionError(LedgerDomainError):
    '''Raised when a transaction's ledger entries do not sum to zero.'''