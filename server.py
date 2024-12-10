from typing import Literal
from flask_cors import CORS
from flask import Flask, jsonify
from flask.wrappers import Response
from blockchain import Blockchain

# Instantiate the blockchain
blockchain = Blockchain()

# Instantiate the server
app = Flask(import_name=__name__)

# Enable CORS
CORS(app=app)

@app.route(rule='/mine', methods=['GET'])
def mine() -> tuple[Response, Literal[200]]:
    response: dict[str, str] = {'message': 'Mine a new block.'}
    
    return jsonify(response), 200

@app.route(rule='/transactions/new', methods=['POST'])
def new_transaction() -> tuple[Response, Literal[201]]:
    response: dict[str, str] = {'message': 'Add a new transaction.'}
    
    return jsonify(response), 201

@app.route(rule='/chain', methods=['GET'])
def full_chain() -> tuple[Response, Literal[200]]:
    response: dict[str, list[dict[str, str | int | float | list[dict[str, str | int]]]] | int] = {
        'chain': [block.to_dict() for block in blockchain.chain],
        'length': len(blockchain.chain)
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)