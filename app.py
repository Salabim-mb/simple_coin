import random
import sys
import requests
import json
from flask import Flask, request, Response, make_response, jsonify
from flask_cors import CORS
import base64
from utils.block import Block
from utils.block_header import BlockHeader
from anytree.exporter import UniqueDotExporter
from anytree import RenderTree
import hashlib

from utils.general.general import GeneralUtil
from utils.node import Node
from utils.messenger.messenger import check_if_message_authentic, verify_sender

app = Flask(__name__)
app.config.from_object(__name__)
app.config['CORS_ALLOW_HEADERS'] = '*'
app.config['CORS_ORIGINS'] = '*'
CORS(app)

node = None

LOCAL_ADDRESS = "http://127.0.0.1"


@app.after_request
def modify_headers(response):
    response.headers['X-Pub-Key'] = base64.b64encode(node.pub_key.to_string()).decode()
    response.headers['Origin'] = node.address
    response.headers['Content-Type'] = "application/json"
    return response


@app.route("/message", methods=["POST", "GET"])
def manage_message():
    if request.method == "POST":
        if random.randint(0, 100) > 85:
            print("Transaction ignored")
            return Response(status=200)
        sender_pub_key = request.headers.get('X-Pub-Key')
        data = json.loads(request.get_data().decode())
        if verify_sender(node.node_list, sender_pub_key) \
                and check_if_message_authentic(data['message'], data['signature'], base64.b64decode(sender_pub_key.encode())):
            print(f"Message from {request.headers.get('Origin')}: \"{data['message']}\".")
            node.wallet.balance += json.loads(data['message'])['outputs'][0]['amount']
            return Response(status=200)
        else:
            return Response(status=403)
    elif request.method == "GET":
        message, signature = GeneralUtil.generate_message_with_signature(node)
        return make_response({
            'message': message,
            'signature': signature
        })


# Endpoints for external use, like testing or postman requesting
@app.route('/register-node-frontend', methods=['POST'])
def register_node():
    node.register_node_in_blockchain(request.json)
    return Response(status=200)


@app.route('/proxy/transfer/<target_port>', methods=['POST'])
def proxy_transfer(target_port):
    target_host = f"{LOCAL_ADDRESS}:{target_port}"
    data = request.get_json()
    try:
        if int(data['amount']) > node.wallet.balance:
            return Response(status=403)
        tran = node.wallet.prepare_transaction_to_send(int(data['amount']))
        print(f"TRANSACTION: Sending {data['amount']} to {target_host}")
        requests.post(url=target_host + "/transfer", json={
            'amount': data['amount'],
            'transfer_id': tran.id,
            "signature": GeneralUtil.get_msg_signature(node, tran.id)
        }, headers={
            'X-Pub-Key': base64.b64encode(node.pub_key.to_string()),
            'Origin': node.address
        })
        node.wallet.balance -= int(data['amount']) + node.wallet.tran_fee
        return Response(status=200)
    except Exception as e:
        print(e)
        return Response(status=400)


@app.route('/proxy/forward-message/<target_port>', methods=["GET"])
def forward_message(target_port):
    target_host = f"{LOCAL_ADDRESS}:{target_port}"
    try:
        message, signature = GeneralUtil.generate_message_with_signature(node)
        res = requests.post(url=target_host + "/message", json={
            'message': message,
            'signature': signature
        }, headers={
            'X-Pub-Key': base64.b64encode(node.pub_key.to_string()),
            'Origin': node.address
        })
        return make_response(jsonify({
            'status': res.status_code
        }))
    except Exception as e:
        return Response(status=403)
###


@app.route('/fetch-node-list', methods=['GET'])
def fetch_node_list():
    res_list = GeneralUtil.generate_unique_node_list(node.node_list, [node.get_data_to_send()])
    return make_response(jsonify(res_list))


@app.route('/print-node-list', methods=['GET'])
def print_node_list():
    node.print_node_list()
    return Response(status=200)


@app.route('/print-orphan-list', methods=['GET'])
def print_orphan_list():
    print("Orphan list (external request):")
    print(node.orphan_list)
    return Response(status=200)


@app.route('/register-node', methods=['POST'])
def update_list():
    node.node_list = GeneralUtil.generate_unique_node_list(node.node_list, request.json)
    return make_response(jsonify(node.node_list))


@app.route('/candidate-block', methods=['POST'])
def candidate_block():
    if random.randint(0, 100) > 85:
        print("Candidate block ignored")
        return Response(status=200)
    req_data = json.loads(request.get_data().decode())
    candidate_block_data = req_data['block']
    sender_pub_key = request.headers['X-Pub-Key']
    # check if payload signature is valid and trusted
    if not verify_sender(node.node_list, sender_pub_key) and not check_if_message_authentic(
            candidate_block_data, req_data['signature'], base64.b64decode(sender_pub_key.encode())
    ):
        print("Incorrect signature of incoming block!")
        return Response(status=403)
    if node.miner.verify_candidate_block(candidate_block_data):
        new_block_header = BlockHeader()
        new_block_header.nonce = candidate_block_data["header"]["nonce"]
        hash_ = candidate_block_data["header"]["previous_block_hash"]
        new_block_header.previous_block_hash = hash_
        parent = None
        for block in node.blockchain.blocks:
            if hashlib.sha256(str(block.as_json()).encode("utf-8")).hexdigest() == hash_:
                parent = block
        new_block = Block(new_block_header, json.loads(candidate_block_data["transactions"]), None)
        node.filter_transaction_pool(candidate_block_data["transactions"])
        if not parent:
            node.orphan_list.append(new_block)
        else:
            new_block.parent = parent
            node.blockchain.blocks.append(new_block)
            node.filter_orphan_list(new_block)
        node.miner.event.set()
    return Response(status=200)


# @app.route('/fetch-blockchain', methods=['GET'])
# def fetch_blockchain():
#     return make_response(node.blockchain.blocks)


@app.route('/fetch-blockchain', methods=['GET'])
def get_candidate_blocks():
    try:
        json_list = []
        for internal_node in node.blockchain.blocks:
            json_list.append(internal_node.as_json())
        return make_response(jsonify(json_list))
    except Exception as e:
        print(e)
        return Response(status=400)


@app.route('/get-balance', methods=['GET'])
def get_wallet_balance():
    return make_response(jsonify({"balance": node.wallet.balance}))


@app.route('/print-blockchain', methods=['GET'])
def print_blockchain():
    print(RenderTree(node.blockchain.blocks[0]))
    UniqueDotExporter(node.blockchain.blocks[0], nodeattrfunc=lambda n: 'label="%s"' % n.name).to_picture(f"tree_{node_name}.png")
    return Response(status=200)


@app.route('/transfer', methods=['POST'])
def transfer_simple_coin():
    try:
        data = request.get_json()
        sender_pk = request.headers.get('X-Pub-Key')
        if verify_sender(node.node_list, sender_pk):
            if check_if_message_authentic(data['transfer_id'], data['signature'], base64.b64decode(sender_pk.encode())):
                node.wallet.create_transaction(int(data['amount']), data['transfer_id'], sender_pk)
                node.wallet.balance += int(data['amount'])
        return Response(status=200)
    except Exception as e:
        print(e)
        print(request.get_json())
        return Response(status=400)


@app.route("/")
def hello_world():
    print(f"Server running: {node.name} on url {node.address}")


if __name__ == '__main__':
    node_name, port = GeneralUtil.parse_args(sys.argv)
    node = Node(node_name, port)
    app.run(port=port)
