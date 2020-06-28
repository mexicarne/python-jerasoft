from .base import JeraSoftAPI


class Rates(JeraSoftAPI):
    def __init__(self, rate_tables_id):
        self.id = rate_tables_id
        super(Rates, self).__init__(rate_tables_id)
        if self.id:
            self.get()

    @classmethod
    def get_object(cls, rate_tables_id):
        rate = cls()
        return rate.get()

    def get(self):
        if not self.id:
            return None

        params = {
            "rate_tables_id": self.id,
            "state": "current",
        }
        data = self.get_data("rates.search", params)
        if data:
            self.rates = data
            return data
        return None

    def by_code(self, code):
        for rate in self.rates:
            if rate.get("code") == code:
                return rate
        return None

    def codes(self):
        return [rate.get("code") for rate in self.rates]

    def __str__(self):
        if self.id:
            return "<Rates: {}>".format(self.id)
