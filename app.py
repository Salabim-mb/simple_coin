import sys
from flask import Flask, request, Response, make_response, jsonify
from flask_cors import CORS, cross_origin

from utils.general.general import parse_args, filter_array_unique_by_param
from utils.local.identity_local import IdentityLocal
from utils.remote.identity_remote import IdentityRemote

app = Flask(__name__)
app.config.from_object(__name__)
app.config['CORS_ALLOW_HEADERS'] = '*'
app.config['CORS_ORIGINS'] = '*'
CORS(app)

id_local = IdentityLocal()
id_remote = IdentityRemote()


@app.route("/message", methods=["POST", "GET"])
@cross_origin()
def manage_message():
    if request.method == "POST":
        return None
    if request.method == "GET":
        return None  # TODO long polling


# Endpoint for external use, like testing or postman requesting
@app.route('/register-node', methods=['POST'])
def register_node():
    id_remote.register_node_in_blockchain(request.json)
    return "ok"


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
