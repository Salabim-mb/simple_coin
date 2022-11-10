from utils.messenger.messenger import sign_message
import datetime

ARG_NUM = 3


class GeneralUtil:

    @staticmethod
    def parse_args(argv: []) -> (int, int):
        """
        Execution params parser
        :param argv: list of execution params
        :return: node name and port
        """
        if len(argv) is not ARG_NUM:
            print(f"Number of arguments must equal {ARG_NUM - 1}")
        return int(argv[1]), int(argv[2])

    @staticmethod
    def generate_unique_node_list(node_list: [], nodes_fetched_to_add: []) -> []:
        """
        Appends to array if new unique values are provided
        :param node_list: array to append to
        :param nodes_fetched_to_add: array of objects that need to be appended
        :return: joined arrays with unique values
        """
        updated_node_list = node_list
        for node in nodes_fetched_to_add:
            updated_node_list = [n for n in updated_node_list if n["name"] != node["name"]]
            updated_node_list.append(node)
        return updated_node_list

    @staticmethod
    def generate_message_with_signature(node) -> (str, str):
        """
        Mock for providing message to post to messenger host
        :param node: instance of ItentityLocal class,
        :return: example message and its signature
        """
        message = f"test message from node {node.name}, {node.address}, created at {datetime.datetime.now()}"
        signature = sign_message(message, node.priv_key).decode('ISO-8859-1')
        return message, signature
