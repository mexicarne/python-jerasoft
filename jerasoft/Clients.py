from .utils import get_stop_date
from .settings import jsconf
from .base import JeraSoftAPI, DataReadError


class Clients(JeraSoftAPI):
    def __init__(self, client_id=None):
        self.id = client_id if client_id else None
        self.name = None
        super(Clients, self).__init__(client_id)
        if self.id:
            self.get()

    @classmethod
    def get_object(cls, client_id):
        """
            Class method that will return a Clients object by its ID
        """
        client = cls()
        client.get()
        return client

    def _set_object(self, data):
        self.balance_accountant = data.get("balance_accountant")
        self.currencies_id = data.get("currencies_id")
        self.low_balance_athreshold = data.get("low_balance_athreshold")
        self.status = data.get("status")
        self.c_email_billing = data.get("c_email_billing")
        self.companies_id = data.get("companies_id")
        self.name = data.get("name")
        self.orig_rate_table = data.get("orig_rate_table")
        self.bill_by_time = data.get("bill_by_time")
        self.credit = data.get("credit")

    def get(self):
        if not self.id:
            return

        params = {"id": self.id}
        data = self.get_data("clients.get", params)
        if data:
            self._set_object(data)
        return data

    def balance(self):
        return self.balance_accountant

    def delete(self):
        # Delete the Client (physically remove)
        if not self.id:
            return
        params = {"id": self.id}
        return self.get_data("clients.delete", params)

    def archive(self):
        # Archive the Client (mark as removed)
        if not self.id:
            return
        params = {"id": self.id}
        return self.get_data("clients.archive", params)

    def create(self, **kw):
        # Create the Client
        default = jsconf.get("default")
        currencies_id = kw.get("currencies_id") or default.get("currencies_id")
        companies_id = kw.get("companies_id") or default.get("companies_id")
        credit = kw.get("credit") or default.get("credit")
        bill_by_time = kw.get("bill_by_time") or default.get("bill_by_time")
        low_balance_athreshold = kw.get("low_balance_athreshold") or default.get(
            "low_balance_athreshold"
        )

        params = {
            "name": "CF: {}".format(kw.get("name").encode("utf-8")),
            "currencies_id": currencies_id,
            "companies_id": companies_id,
            "bill_by_time": bill_by_time,
            "credit": credit,
            "c_company": kw.get("c_company").encode("utf-8"),
            "c_email_billing": kw.get("c_email_billing").encode("utf-8"),
            "low_balance_athreshold": low_balance_athreshold,
        }

        try:
            data = self.get_data("clients.create", params=params)
            self.id = data.get("id")
            self.get()
            return (True, data.get("id"))
        except DataReadError as exc:
            return (False, str(exc))

    def add_package(self, **kwargs):
        if not self.id:
            return

        default = jsconf.get("default")
        stop_days = kwargs.get("stop_days") or default.get("stop_days")
        packages_id = kwargs.get("packages_id") or default.get("packages_id")

        stop_dt = get_stop_date(stop_days)
        params = {
            "clients_id": self.id,
            "packages_id": packages_id,
            "stop_dt": stop_dt,
        }
        try:
            data = self.get_data("clients_packages.assign", params=params)
            return (True, "")
        except DataReadError as exc:
            return (False, str(exc))

    def update(self, **kwargs):
        if not self.id:
            return

        params = {"id": self.id}
        if kwargs:
            params.update(kwargs)
        try:
            data = self.get_data("clients.update", params=params)
            self.get()
            return (True, "")
        except DataReadError as exc:
            return (False, str(exc))

    def __str__(self):
        if self.id and self.name:
            name = self.name.encode("utf-8")
            return "<Clients: {} {} {}>".format(self.id, name, self.balance())
        else:
            return "<Clients: Not found>"
