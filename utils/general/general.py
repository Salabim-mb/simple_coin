ARG_NUM = 3


class GeneralUtil:

    @staticmethod
    def parse_args(argv) -> (int, int):
        """
        Static method for parsing application input arguments.
        2 arguments for node name and port are required.
        :param argv:
        :return:
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
    def get_sample_message(id_local, sign_message) -> (str, str):
        """
        Creates sample message with its signature
        :param id_local:
        :param sign_message:
        :return:
        """
        message = f"test message from node {id_local.name} (address: {id_local.address})"
        signature = sign_message(message, id_local.priv_key).decode('ISO-8859-1')
        return message, signature
