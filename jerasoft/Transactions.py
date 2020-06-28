from .settings import jsconf
from .base import JeraSoftAPI, DataReadError


class Transactions(JeraSoftAPI):
    def __init__(self, client_id):
        self.id = client_id
        self.counted = None
        super(Transactions, self).__init__(client_id)
        if self.id:
            self.get()

    @classmethod
    def get_object(cls, client_id):
        """
            Class method that will return a Clients object by its ID
        """
        trans = cls()
        trans.get()
        return trans

    def get(self, limit=0):
        if not self.id:
            return

        params = {
            "clients_id": self.id,
        }

        if limit > 0:
            params["limit"] = limit

        data = self.get_data("transactions.search", params)
        if data:
            self.raw_charges = data
            self.charges_extract()
            return (self.charges, self.counted)

    def charges_extract(self):
        charges = []
        for charge in self.raw_charges:
            charges.append(
                {
                    "date": charge.get("c_dt"),
                    "amount": charge.get("amount"),
                    "comment": charge.get("notes"),
                }
            )
        self.counted = sum(c.get("amount") for c in charges)
        self.charges = charges

    def __str__(self):
        if self.id:
            return "<Transactions {} {}>".format(self.id, self.counted)
