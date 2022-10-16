import sys
import requests
from flask import Flask, request, Response, make_response, jsonify
from flask_cors import CORS

from utils.general.general import parse_args, filter_array_unique_by_param
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
    response.headers['pub_key'] = id_local.pub_key.to_pem().decode()
    response.headers['Origin'] = id_local.address
    return response


@app.route("/message", methods=["POST"])
def manage_message():
    if request.method == "POST":
        sender_pub_key = request.headers.get('pub_key')
        response = request.json
        if verify_sender(id_remote, sender_pub_key) \
                and check_if_message_authentic(response['message'], response['signature'], sender_pub_key):
            print(f"Message from {request.headers.get('Origin')}: {response['message']}")
            return Response(status=200)
        else:
            return Response(status=403)
    elif request.method == "GET":
        message = "test message"
        signature = sign_message(message, id_local.priv_key)
        return make_response(jsonify({
            'message': message,
            signature: signature
        }))


# Endpoints for external use, like testing or postman requesting
@app.route('/proxy/register-node', methods=['POST'])
def register_node():
    id_remote.register_node_in_blockchain(request.json)
    return "ok"


@app.route('/proxy/forward-message/<target_port>', methods=["GET"])
def forward_message(target_port):
    target_host = f"{LOCAL_ADDRESS}:{target_port}"
    try:
        response = requests.get(url=target_host + "/message")
        requests.post(url=id_local.address, json=response.json)
        return Response(status=200)
    except Exception as e:
        return Response(status=403)
###


@app.route('/fetch-node-list', methods=['GET'])
def fetch_node_list():
    res_list = filter_array_unique_by_param(id_remote.node_list, [id_local.get_data_to_send()], 'name')
    return make_response(jsonify(res_list))


@app.route('/print-node-list', methods=['GET'])
def print_node_list():
    id_remote.print_node_list()
    return Response(status=200)


@app.route('/update-node-list', methods=['POST'])
def update_list():
    id_remote.node_list = filter_array_unique_by_param(id_remote.node_list, request.json, 'name')
    return make_response(jsonify(id_remote.node_list))


@app.route("/")
def hello_world():
    print(f"Server running: {id_local.name} on url {id_local.address}")


if __name__ == '__main__':
    node_name, port = parse_args(sys.argv)
    id_local.set_node_basic_data(node_name, port)
    id_local.get_ssh_pair()
    id_remote.register_node_in_blockchain(id_local.get_data_to_send())
    id_remote.update_list()
    app.run(port=port)
