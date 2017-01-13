from __future__ import absolute_import

import json
import logging

import websocket

import dockercloud
from .base import StreamingAPI
from .exceptions import AuthError

logger = logging.getLogger("python-dockercloud")


class Events(StreamingAPI):
    def __init__(self, namespace=""):
        endpoint = "events"

        if not namespace:
            namespace = dockercloud.namespace
        if namespace:
            url = "/".join([dockercloud.stream_host.rstrip("/"), "api", "audit", self._api_version,
                            namespace, endpoint.lstrip("/")])
        else:
            url = "/".join([dockercloud.stream_host.rstrip("/"), "api", "audit", self._api_version,
                            endpoint.lstrip("/")])
        super(self.__class__, self).__init__(url)

    def _on_message(self, ws, message):
        logger.info("Websocket Message: %s" % message)
        try:
            event = json.loads(message)
        except ValueError:
            return
        if event.get("type") == "auth":
            return

        if self.message_handler:
            self.message_handler(message)

    def _on_error(self, ws, e):
        if isinstance(e, websocket._exceptions.WebSocketBadStatusException) and getattr(e, "status_code") == 401:
            self.auth_error = True

        super(self.__class__, self)._on_error(ws, e)

    def run_forever(self, *args, **kwargs):
        while True:
            if self.auth_error:
                self.auth_error = False
                raise AuthError("Not Authorized")

            ws = websocket.WebSocketApp(self.url, header=self.header,
                                        on_open=self._on_open,
                                        on_message=self._on_message,
                                        on_error=self._on_error,
                                        on_close=self._on_close)
            ws.run_forever(ping_interval=10, ping_timeout=5, *args, **kwargs)
