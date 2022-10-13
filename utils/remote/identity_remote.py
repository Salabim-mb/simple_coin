class IdentityRemote:
    def __init__(self):
        self.pub_list: [str] = []   # only public keys are stored - those are the base for authentication

    def print_pub_list(self) -> None:
        print(self.pub_list)

    # TODO typowanie argumentu new_entry
    def add_to_pub_list(self, new_entry: str) -> None:
        self.pub_list.append(new_entry)

    def remove_from_pub_list(self, entry: str) -> None:
        self.pub_list.remove(entry)