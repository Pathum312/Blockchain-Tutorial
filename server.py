from typing import Literal
from uuid import uuid4

from blockchain import Block, Blockchain, BlockDict, TransactionDict
from flask import Flask, jsonify, request
from flask.wrappers import Response

# from textwrap import dedent
from flask_cors import CORS

# Instantiate the blockchain
blockchain = Blockchain()

# Generate a globally unique address for this node
node_identifier: str = str(object=uuid4()).replace("-", "")

# Instantiate the server
app = Flask(import_name=__name__)

# Enable CORS
CORS(app=app)


@app.route(rule="/mine", methods=["GET"])
def mine() -> tuple[Response, Literal[200]]:
    # Get the last block
    last_block: Block = blockchain.last_block

    # Get the proof of the last block
    last_proof: int = last_block.proof

    # Get the next proof of work
    proof: int = blockchain.proof_of_work(last_proof=last_proof)

    # A reward must be issued to the miner
    blockchain.new_transaction(
        sender="0",  # Sender is "0" to signify that this node has mined a new block
        recipient=node_identifier,  # Recipient is the node identifier
        amount=1,  # Reward
    )

    # Get the hash of the last block
    previous_hash: str = blockchain.hash(block=last_block)

    # Create a new block
    block: Block = blockchain.new_block(proof=proof, previous_hash=previous_hash)

    # Convert the block to a dictionary
    formatted_block: BlockDict = block.to_dict()

    response: dict[str, str | int | float | list[TransactionDict] | None] = {
        "message": "New Block Forged",
        "index": formatted_block.get("index"),
        "transactions": formatted_block.get("transactions"),
        "proof": formatted_block.get("proof"),
        "previous_hash": formatted_block.get("previous_hash"),
    }

    return jsonify(response), 200


@app.route(rule="/transactions/new", methods=["POST"])
def new_transaction() -> tuple[Response, Literal[201] | Literal[400]]:
    # Get the request payload
    payload: dict[str, str | int] = request.get_json()

    # Check if all the required fields are present
    required: list[str] = ["sender", "recipient", "amount"]
    for field in required:
        if not payload.get(field):
            return (
                jsonify(
                    {
                        "message": f"{f'{field}s address' if field != 'amount' else field} is required."
                    }
                ),
                400,
            )

    # Create a new transaction
    index: int = blockchain.new_transaction(
        sender=payload.get("sender"),  # type: ignore
        recipient=payload.get("recipient"),  # type: ignore
        amount=payload.get("amount"),  # type: ignore
    )

    response: dict[str, str] = {
        "message": f"Transaction will be added to Block {index}."
    }

    return jsonify(response), 201


@app.route(rule="/chain", methods=["GET"])
def full_chain() -> tuple[Response, Literal[200]]:
    response: dict[str, list[BlockDict] | int] = {
        "chain": [block.to_dict() for block in blockchain.chain],
        "length": len(blockchain.chain),
    }

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
