class Input:
    def __init__(self, prev_owner_id, curr_owner_pk, amount):
        self.prev_id = prev_owner_id
        self.curr_owner_pk = curr_owner_pk
        self.amount = amount

    def as_json(self) -> {}:
        return {
            "prev_id": self.prev_id,
            "curr_owner_pk": self.curr_owner_pk,
            "amount": self.amount
        }
