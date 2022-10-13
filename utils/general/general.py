ARG_NUM = 3


def parse_args(argv) -> (int, int):
    if len(argv) is not ARG_NUM:
        print(f"Number of arguments must equal {ARG_NUM - 1}")
    return int(argv[1]), int(argv[2])
