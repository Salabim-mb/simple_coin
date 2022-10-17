ARG_NUM = 3


def parse_args(argv) -> (int, int):
    if len(argv) is not ARG_NUM:
        print(f"Number of arguments must equal {ARG_NUM - 1}")
    return int(argv[1]), int(argv[2])


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
