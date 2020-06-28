from .utils import convert_date
from .base import JeraSoftAPI, DataReadError


class Reports(JeraSoftAPI):
    def __init__(self, accounts_id):
        self.accounts_id = accounts_id
        super(Reports, self).__init__(accounts_id)

    @classmethod
    def get_object(cls, client_id):
        report = cls()
        return report.get()

    def get(self, start=None, end=None):
        dates = (convert_date(start, "start"), convert_date(end, "end"))
        params = {
            "accounts_id": [self.accounts_id],
            "dt": dates,
        }
        result = self.get_data("reports.xdrs", params)
        # TODO: needs parsing. No real data at the moment
        return result

    def __str__(self):
        if self.accounts_id:
            return "<Reports: {}>".format(self.accounts_id)
        else:
            return "<Reports: Not found>"
