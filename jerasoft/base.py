import os
import uuid
import logging
import requests
from settings import jsconf


class Error(Exception):
    pass


class TokenError(Error):
    pass


class DataReadError(Error):
    pass


class JSONReadError(Error):
    pass


class WrongRequestIdError(Error):
    pass


class JeraSoftAPI(object):
    """
        Basic api class for JeraSoft VSC API
    """

    def __init__(self, *args, **kwargs):
        self.token = jsconf.get("token")
        self.endpoint = jsconf.get("endpoint")
        self._log = logging.getLogger(__name__)
        self.request_id = uuid.uuid4().hex

        for attr in kwargs:
            setattr(self, attr, kwargs[attr])

    def __perform_request(self, params=None):
        if params is None:
            params = {}

        if not self.token:
            raise TokenError("No token is provided. Please use a valid token")

        payload = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": self.method,
            "params": {"AUTH": self.token},
        }
        payload["params"].update(params)
        self._log.debug("{}:{} {}", payload, params)

        return requests.post(self.endpoint, json=payload)

    def get_data(self, method, params=None):
        if params is None:
            params = dict()

        self.method = method
        req = self.__perform_request(params)

        try:
            data = req.json()
        except ValueError as e:
            raise JSONReadError("Read failed from JeraSoft VCS: {}".format(str(e)))

        if data.get("id") != self.request_id:
            raise WrongRequestIdError

        if "error" in data:
            msg = data.get("error")["message"]
            raise DataReadError(msg)

        return data.get("result")

    def __str__(self):
        return "<{}>".format(self.__class__.__name__)

    def __unicode__(self):
        return u"{}".format(self.__str__())

    def __repr__(self):
        return str(self)
