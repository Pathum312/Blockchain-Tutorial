from typing import Literal

from blockchain import Blockchain, BlockDict
from flask import Flask, jsonify, request
from flask.wrappers import Response

# from textwrap import dedent
from flask_cors import CORS

# Instantiate the blockchain
blockchain = Blockchain()

# Instantiate the server
app = Flask(import_name=__name__)

# Enable CORS
CORS(app=app)


@app.route(rule="/mine", methods=["GET"])
def mine() -> tuple[Response, Literal[200]]:
    response: dict[str, str] = {"message": "Mine a new block."}

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
