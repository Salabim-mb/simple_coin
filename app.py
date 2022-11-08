import sys
import requests
import json
from flask import Flask, request, Response, make_response, jsonify
from flask_cors import CORS
import base64

from utils.general.general import GeneralUtil
from utils.node import Node
from utils.messenger.messenger import check_if_message_authentic, verify_sender, sign_message

app = Flask(__name__)
app.config.from_object(__name__)
app.config['CORS_ALLOW_HEADERS'] = '*'
app.config['CORS_ORIGINS'] = '*'
CORS(app)

node = Node()

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
        sender_pub_key = request.headers.get('X-Pub-Key')
        data = json.loads(request.get_data().decode())
        if verify_sender(node.node_list, sender_pub_key) \
                and check_if_message_authentic(data['message'], data['signature'], base64.b64decode(sender_pub_key.encode())):
            print(f"Message from {request.headers.get('Origin')}: {data['message']}")
            return Response(status=200)
        else:
            return Response(status=403)
    elif request.method == "GET":
        message, signature = GeneralUtil.get_sample_message(node, sign_message)
        return make_response({
            'message': message,
            'signature': signature
        })


# Endpoints for external use, like testing or postman requesting
@app.route('/register-node', methods=['POST'])
def register_node():
    node.register_node_in_blockchain(request.json)
    return Response(status=200)


@app.route('/proxy/forward-message/<target_port>', methods=["GET"])
def forward_message(target_port):
    target_host = f"{LOCAL_ADDRESS}:{target_port}"
    try:
        message, signature = GeneralUtil.get_sample_message(node, sign_message)
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
    res_list = GeneralUtil.filter_array_unique_by_param(node.node_list, [node.get_data_to_send()], 'name')
    return make_response(jsonify(res_list))


@app.route('/print-node-list', methods=['GET'])
def print_node_list():
    node.print_node_list()
    return Response(status=200)


@app.route('/update-node-list', methods=['POST'])
def update_list():
    node.node_list = GeneralUtil.filter_array_unique_by_param(node.node_list, request.json, 'name')
    return make_response(jsonify(node.node_list))


@app.route("/")
def hello_world():
    print(f"Server running: {node.name} on url {node.address}")


if __name__ == '__main__':
    node_name, port = GeneralUtil.parse_args(sys.argv)
    node.set_node_basic_data(node_name, port)
    node.get_ssh_pair()
    node.register_node_in_blockchain(node.get_data_to_send())
    node.update_list()
    app.run(port=port)
