from utils.wallet.Transaction import Transaction


class Wallet:
    """
    class for managing coin transfers between nodes
    """

    def __init__(self, node):
        self.node = node
        self.balance = 100      # for testing purposes
        self.transactions: [Transaction] = []

    def create_transaction(self, amount: int, transaction_id: str, prev_owner_pk: str) -> None:
        """
        Creates new transaction
        :param amount: money sent
        :param transaction_id: id for comparison and forwarding
        :param prev_owner_pk: public key for authentication
        :return: None
        """
        tran = Transaction()
        tran.create_input(amount, transaction_id, prev_owner_pk)
        self.transactions.append(tran)

    def prepare_transaction_to_send(self, amount: int) -> Transaction:
        """
        Creates transaction output before sending
        :param amount: amount to note in transaction
        :return: Updated transaction object
        """
        current_tran = self.transactions.pop()
        current_tran.create_output(amount, str(self.node.pub_key))
        self.transactions.append(current_tran)
        return current_tran


