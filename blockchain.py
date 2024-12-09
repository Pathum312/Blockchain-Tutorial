
class Transaction:
    """
    Transaction class
    
    Attributes:
        sender (str): Address of the sender
        recipient (str): Address of the recipient
        amount (int): Transaction amount
    """
    def __init__(self, sender: str, recipient: str, amount: int) -> None:
        """
        Initializes a new transaction
        
        Parameters:
            sender (str): Address of the sender
            recipient (str): Address of the recipient
            amount (int): Transaction amount
        
        Returns:
            None
        """
        self.sender: str = sender # Address of the sender
        self.recipient: str = recipient # Address of the recipient
        self.amount: int = amount # Transaction amount

class Block:
    """
    Block class
    
    Attributes:
        index (int): Index of the block
        timestamp (int): Timestamp
        transactions (list[Transaction]): List of transactions in the block
        proof (int): Proof of work
        previous_hash (str): Hash of the previous block
    """
    def __init__(
        self, 
        index: int, 
        timestamp: int, 
        transactions: list[Transaction], 
        proof: int, 
        previous_hash: str
        ) -> None:
        """
        Initializes a new block
        
        Parameters:
            index (int): Index of the block
            timestamp (int): Timestamp
            transactions (list[Transaction]): List of transactions in the block
            proof (int): Proof of work
            previous_hash (str): Hash of the previous block
        
        Returns:
            None
        """
        self.index: int = index # Index of the block
        self.timestamp: int = timestamp # Timestamp
        self.transactions: list[Transaction] = transactions # List of transactions in the block
        self.proof: int = proof # Proof of work
        self.previous_hash: str = previous_hash # Hash of the previous block

class Blockchain:
    """
    Blockchain class
    
    Attributes:
        chain (list[Block]): List of blocks
        current_transactions (list[Transaction]): List of transactions
    """
    def __init__(self) -> None:
        self.chain: list[Block] = [] # List of blocks
        self.current_transactions: list[Transaction] = [] # List of transactions
    
    def new_block(self):
        # Creates a new Block and adds it to the chain
        ...
    
    def new_transaction(self, sender: str, recipient: str, amount: int) -> int:
        """
        Creates a new transaction to go into the next mined Block
        
        Parameters:
            sender (str): Address of the sender
            recipient (str): Address of the recipient
            amount (int): Transaction amount
        
        Returns:
            int: The index of the Block that will hold this transaction
        """
        # Create a new transaction
        transaction = Transaction(sender=sender, recipient=recipient, amount=amount)
        
        # Add the new transaction to the list of transactions
        self.current_transactions.append(transaction)
        
        # Returns the index of the block that will hold this transaction
        return self.last_block.index + 1
    
    @staticmethod
    def hash(block: Block) -> str:
        # Hashes a block
        ...
    
    @property
    def last_block(self) -> Block:
        # Returns the last Block in the chain
        ...