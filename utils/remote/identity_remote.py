import requests
from utils.general.general import filter_array_unique_by_param

LOCAL_ADDRESS = "http://127.0.0.1"
searchable_port_suf = range(5001, 5011)     # Port range to search addresses


class IdentityRemote:
    def __init__(self):
        self.node_list: [] = []   # only public keys are stored - those are the base for authentication

    def print_node_list(self) -> None:
        """
        Prints list of nodes in blockchain
        :return:
        """
        print("Current node list:", self.node_list)

    def update_list(self) -> None:
        """
        Update list of nodes by fetching it from other nodes. Used after app startup
        :return:
        """
        for node in self.node_list:
            host = node['address']
            try:
                response = requests.get(url=(host + "/fetch-node-list"))
                print(f"Found node with url {host}.")
                self.node_list = filter_array_unique_by_param(self.node_list, response.json(), 'name')
                break
            except Exception as e:
                print(f"Error with node {host}, couldn't find active target host. {str(e)}")

    def register_node_in_blockchain(self, item: {} = None) -> None:
        """
        Add new node to blockchain and broadcast updated list of nodes to other nodes to let them update it too
        :param item: Node to append and broadcast through network
        :return:
        """
        if item is not None:
            self.node_list.append(item)
        for port in searchable_port_suf:
            host = f"{LOCAL_ADDRESS}:{port}"
            if host == item['address']:
                continue
            try:
                res = requests.post(url=(host + "/update-node-list"), json=self.node_list)
                self.node_list = filter_array_unique_by_param(self.node_list, res.json(), 'name')
            except Exception as e:
                print(f"Error with node {host}, couldn't find active target host. {str(e)}")
