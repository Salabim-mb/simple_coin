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
    def filter_array_unique_by_param(acc: [], to_add: [], param_name: str) -> []:
        """
        Appends to array if new unique values are provided
        :param acc: array to append to
        :param to_add: array of objects that need to be appended
        :param param_name: parameter name that should be unique
        :return: joined arrays with unique values
        """
        new_acc = acc
        for node in to_add:
            new_acc = [n for n in new_acc if n[param_name] != node[param_name]]
            new_acc.append(node)
        return new_acc

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
