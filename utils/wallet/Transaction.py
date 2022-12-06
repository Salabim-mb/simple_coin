from utils.wallet.Output import Output
import random

from utils.wallet.Input import Input


class Transaction:
    """
    Definition of transaction in wallet and block mining
    """

    def __init__(self):
        self.outputs: [Output] = []
        self.inputs: [Input] = []
        self.fee = 1    # needs adjusting maybe
        self.id = "%032x" % random.getrandbits(256)
        self.total_amount = None

    def get_own_outputs(self, own_pk) -> [Output]:
        """
        As a preparation for transaction, get outputs concerning current node
        :param: own_pk: own public key
        :return: list of outputs that are assigned to current user
        """
        pass

    def filter_outputs(self) -> None:
        """
        Deletes all outputs that are spent and present in input list from output list
        :return: None
        """
        filtered_outputs = []
        for out in self.outputs:
            if out.is_spent is False and out.new_owner_pk not in map(lambda inp: inp.curr_owner_pk, self.inputs):
                filtered_outputs.append(out)
        self.outputs = filtered_outputs

    def create_input(self, amount: int, prev_id: str, curr_owner: str) -> None:
        """
        incoming request handler
        creates inputs based on filtered outputs from
        :return: None
        """
        self.inputs.append(Input(prev_id, curr_owner, amount))

    def create_output(self, amount: int, owner_pk: str) -> None:
        """
        output preparation to send to coin recipient
        :param amount: output amount
        :param owner_pk: from whom does the amount come
        :return: None
        """
        self.outputs.append(Output(owner_pk, amount - self.fee))
