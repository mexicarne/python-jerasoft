from .settings import jsconf
from .base import JeraSoftAPI


class Accounts(JeraSoftAPI):
    def __init__(self, account_id=None):
        self.id = account_id if account_id else None
        self.name = None
        super(Accounts, self).__init__(account_id)
        if self.id:
            self.get()

    @classmethod
    def get_object(cls, account_id):
        account = cls()
        return account.get()

    def _set_object(self, data):
        self.ani = data.get("ani")
        self.auth_type = data.get("auth_type")
        self.clients_id = data.get("clients_id")
        self.clients_name = data.get("clients_name")
        self.ips = data.get("ips")
        self.name = data.get("name")
        self.orig_enabled = data.get("orig_enabled")
        self.orig_rate_table = data.get("orig_rate_table")

    def get(self):
        if not self.id:
            return None

        params = {"id": self.id}
        data = self.get_data("accounts.search", params)
        if data:
            self._set_object(data[0])
            return data[0]
        return None

    def delete(self):
        if not self.id:
            return

        params = {"id": self.id}
        try:
            self.get_data("accounts.delete", params)
            return (True, "")
        except Exception as exc:
            return (False, str(exc))

    def update(self, **kwargs):
        if not self.id:
            return

        params = {"id": self.id}
        if kwargs:
            params.update(kwargs)
        try:
            data = self.get_data("accounts.update", params)
            self.get()
            return (True, "")
        except Exception as exc:
            return (False, str(exc))

    def create(self, **kw):
        default = jsconf.get("default")
        auth_type = kw.get("auth_type") or default.get("auth_type")
        orig_enabled = kw.get("orig_enabled") or default.get("orig_enabled")
        orig_rate_table = kw.get("orig_rate_table") or default.get("orig_rate_table")

        params = {
            "clients_id": kw.get("clients_id"),
            "ani": kw.get("ani"),
            "name": "{} {}".format(kw.get("ipaddr"), kw.get("name")),
            "auth_type": auth_type,
            "orig_enabled": orig_enabled,
            "orig_rate_table": orig_rate_table,
        }
        try:
            data = self.get_data("accounts.create", params=params)
            self.id = data.get("id")
            self.get()
            return (True, self.id)
        except Exception as exc:
            return (False, str(exc))
        return params

    def __str__(self):
        if self.id and self.name:
            name = self.name.encode("utf-8")
            return "<Accounts: {} {}>".format(self.id, name)
        else:
            return "<Clients: Not found>"
