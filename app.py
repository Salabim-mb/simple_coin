import sys
import requests
import json
from flask import Flask, request, Response, make_response, jsonify
from flask_cors import CORS
import base64

from utils.general.general import GeneralUtil
from utils.local.identity_local import IdentityLocal
from utils.remote.identity_remote import IdentityRemote
from utils.remote.messenger import check_if_message_authentic, verify_sender, sign_message

app = Flask(__name__)
app.config.from_object(__name__)
app.config['CORS_ALLOW_HEADERS'] = '*'
app.config['CORS_ORIGINS'] = '*'
CORS(app)

id_local = IdentityLocal()
id_remote = IdentityRemote()

LOCAL_ADDRESS = "http://127.0.0.1"


@app.after_request
def modify_headers(response):
    response.headers['X-Pub-Key'] = base64.b64encode(id_local.pub_key.to_string()).decode()
    response.headers['Origin'] = id_local.address
    response.headers['Content-Type'] = "application/json"
    return response


@app.route("/message", methods=["POST", "GET"])
def manage_message():
    if request.method == "POST":
        sender_pub_key = request.headers.get('X-Pub-Key')
        data = json.loads(request.get_data().decode())
        if verify_sender(id_remote.node_list, sender_pub_key) \
                and check_if_message_authentic(data['message'], data['signature'], base64.b64decode(sender_pub_key.encode())):
            print(f"Message from {request.headers.get('Origin')}: {data['message']}")
            return Response(status=200)
        else:
            return Response(status=403)
    elif request.method == "GET":
        message, signature = GeneralUtil.get_sample_message(id_local, sign_message)
        return make_response({
            'message': message,
            'signature': signature
        })


# Endpoints for external use, like testing or postman requesting
@app.route('/register-node', methods=['POST'])
def register_node():
    id_remote.register_node_in_blockchain(request.json)
    return "ok"


@app.route('/proxy/forward-message/<target_port>', methods=["GET"])
def forward_message(target_port):
    target_host = f"{LOCAL_ADDRESS}:{target_port}"
    try:
        message, signature = GeneralUtil.get_sample_message(id_local, sign_message)
        res = requests.post(url=target_host + "/message", json={
            'message': message,
            'signature': signature
        }, headers={
            'X-Pub-Key': base64.b64encode(id_local.pub_key.to_string()),
            'Origin': id_local.address
        })
        return make_response(jsonify({
            'status': res.status_code
        }))
    except Exception as e:
        return Response(status=403)
###


@app.route('/fetch-node-list', methods=['GET'])
def fetch_node_list():
    res_list = GeneralUtil.filter_array_unique_by_param(id_remote.node_list, [id_local.get_data_to_send()], 'name')
    return make_response(jsonify(res_list))


@app.route('/print-node-list', methods=['GET'])
def print_node_list():
    id_remote.print_node_list()
    return Response(status=200)


@app.route('/update-node-list', methods=['POST'])
def update_list():
    id_remote.node_list = GeneralUtil.filter_array_unique_by_param(id_remote.node_list, request.json, 'name')
    return make_response(jsonify(id_remote.node_list))


@app.route("/")
def hello_world():
    print(f"Server running: {id_local.name} on url {id_local.address}")


if __name__ == '__main__':
    node_name, port = GeneralUtil.parse_args(sys.argv)
    id_local.set_node_basic_data(node_name, port)
    id_local.get_ssh_pair()
    id_remote.register_node_in_blockchain(id_local.get_data_to_send())
    id_remote.update_list()
    app.run(port=port)
