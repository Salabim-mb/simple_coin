import requests

initial_node_list = [
    {
        "name": "5002",
        "address": "http://127.0.0.1:5002",
        "pub_key": "smth2" # TODO add initial pub key from some file
    },
    {
        "name": "5003",
        "address": "http://127.0.0.1:5003",
        "pub_key": "smth3" # TODO add initial pub key from some file
    },
    {
        "name": "5004",
        "address": "http://127.0.0.1:5004",
        "pub_key": "smth4" # TODO add initial pub key from some file
    }
]


class IdentityRemote:
    def __init__(self):
        self.node_list: [] = initial_node_list   # only public keys are stored - those are the base for authentication

    def print_node_list(self) -> None:
        """
        Prints list of nodes in blockchain
        :return:
        """
        print(self.node_list)

    def update_list(self) -> None:
        """
        Update list of nodes by fetching it from other nodes. Used after app startup
        :return:
        """
        for node in self.node_list:
            try:
                response = requests.get(url=(node["address"] + "/fetch-node-list"))
                self.node_list = response.json()
                break
            except Exception as e:
                print(f"error with node {node['name']}, error {str(e)}")

    def register_node_in_blockchain(self, request: {}) -> None:
        """
        Add new node to blockchain and broadcast updated list of nodes to other nodes to let them update it too
        :param request:
        :return:
        """
        item = request.json
        self.node_list.append(item)
        for node in self.node_list:
            try:
                requests.post(url=(node["address"] + "/update-node-list"), json=self.node_list)
            except Exception as e:
                print(f"error with node {node['name']}, error {str(e)}")
