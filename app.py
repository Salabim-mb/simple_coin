import sys
from flask import Flask, request, Response
from flask_cors import CORS, cross_origin

from utils.general.general import parse_args
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


@app.route('/register-node', methods=['POST'])
def register_node():
    id_remote.register_node_in_blockchain(request)
    return "ok"


@app.route('/fetch-node-list', methods=['GET'])
def fetch_node_list():
    return id_remote.node_list


@app.route('/print-node-list', methods=['GET'])
def print_node_list():
    id_remote.print_node_list()
    return Response(status=200)


@app.route('/update-node-list', methods=['POST'])
def update_list():
    id_remote.node_list = request.json
    return Response(status=200)


if __name__ == '__main__':
    node_name, port = parse_args(sys.argv)
    id_local.set_node_basic_data(node_name, port)
    id_local.generate_ssh_pair()
    id_remote.update_list()
    app.run(port=port)
