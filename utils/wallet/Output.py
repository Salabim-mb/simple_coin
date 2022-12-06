class Output:
    def __init__(self, new_owner, amount):
        self.new_owner_pk = new_owner
        self.amount = amount
        self.is_spent = False       # on init the amount is not spent
