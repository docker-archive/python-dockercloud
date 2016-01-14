from __future__ import absolute_import

from .base import Mutable
from .exceptions import ApiError
from .http import send_request


class Stack(Mutable):
    subsystem = "app"
    endpoint = "/stack"

    def start(self):
        return self._perform_action("start")

    def stop(self):
        return self._perform_action("stop")

    def redeploy(self, reuse_volumes=True):
        params = {'reuse_volumes': reuse_volumes}
        return self._perform_action("redeploy", params=params)

    def export(self):
        if not self._detail_uri:
            raise ApiError("You must save the object before performing this operation")
        url = "/".join([self._detail_uri, "export"])
        return send_request("GET", url, inject_header=False)
