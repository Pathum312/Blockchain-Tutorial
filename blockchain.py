import json
import hashlib
from time import time

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
        timestamp: float, 
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
        self.timestamp: float = timestamp # Timestamp
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
        
        # Create the genesis block
        self.new_block(proof=100, previous_hash='1')
    
    def new_block(self, proof: int, previous_hash: str | None = None) -> Block:
        """
        Creates a new block in the blockchain
        
        Parameters:
            proof (int): Proof of work
            previous_hash (str | None): Hash of the previous block
        
        Returns:
            Block: The new block
        """
        # Create a new block
        block = Block(
            index=len(self.chain) + 1,
            timestamp=time(),
            transactions=self.current_transactions,
            proof=proof,
            previous_hash=previous_hash or self.hash(block=self.chain[-1])
        )
        
        # Reset the current list of transactions
        self.current_transactions = []
        
        # Add the block to the chain
        self.chain.append(block)
        
        # Return the new block
        return block
    
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
        """
        Creates a SHA-256 hash of a Block
        
        Parameters:
            block (Block): Block to hash
        
        Returns:
            str: Hash of the block
        """
        # Make sure the dictionary is ordered, or we'll have inconsistent hashes
        block_string: bytes = json.dumps(obj=block, sort_keys=True).encode()
        return hashlib.sha256(string=block_string).hexdigest()
    
    def proof_of_work(self, last_proof: int) -> int:
        """
        Simple Proof of Work Algorithm:
        - Find a number p' such that hash(p, p') contains leading 4 zeroes.
        - p is the previous proof, p' is the new proof.
        
        Parameters:
            last_proof (int): Previous Proof (p)
        
        Returns:
            int: New Proof (p')
        """
        proof: int = 0
        
        while self.validate_proof(last_proof=last_proof, proof=proof) is False:
            proof += 1
        
        return proof
        
    @staticmethod
    def validate_proof(last_proof: int, proof: int) -> bool:
        """
        Validates a Proof to see if the hash has 4 leading zeroes
        
        Parameters:
            last_proof (int): Previous Proof
            proof (int): Current Proof
        
        Returns:
            bool: True if correct, False if not
        """
        # Encode the last proof and the current proof
        guess: bytes = f'{last_proof}{proof}'.encode()
        
        # Hash the guess with SHA-256
        guess_hash: str = hashlib.sha256(string=guess).hexdigest()
        
        # Check if the guess hash has 4 leading zeroes
        return guess_hash[:4] == '0000'
    
    @property
    def last_block(self) -> Block:
        """
        Returns the last Block in the chain
        
        Returns:
            Block: The last Block in the chain
        """
        # Returns the last Block in the chain
        return self.chain[-1]