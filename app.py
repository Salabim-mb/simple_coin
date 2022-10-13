import sys
from flask import Flask, request, make_response
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


@app.before_request
def check_header() -> None:
    """
    Check if header with pub key is present and assign it to g, otherwise deny connection
    :return:
    """
    return None # TODO


@app.after_request
def add_headers(response: {}) -> {}:
    response.headers['self-identity'] = ""  # TODO
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/message", methods=["POST", "GET"])
@cross_origin()
def manage_message():
    if request.method == "POST":
        return None
    if request.method == "GET":
        return None   # TODO long polling


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    node_number, port = parse_args(sys.argv)
    app.run(port=5000)
