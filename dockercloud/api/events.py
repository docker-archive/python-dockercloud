from __future__ import absolute_import

import json

import websocket

import dockercloud
from .base import StreamingAPI
from .exceptions import AuthError


class Events(StreamingAPI):
    def __init__(self):
        endpoint = "events"
        url = "/".join([dockercloud.stream_host.rstrip("/"), "api", "audit", self._api_version, endpoint.lstrip("/")])
        super(self.__class__, self).__init__(url)

    def _on_message(self, ws, message):
        print message
        try:
            event = json.loads(message)
        except ValueError:
            return

        if event.get("type") == "error" and event.get("data", {}).get("errorMessage", "") in\
                ["Incorrect authentication credentials.", "Unauthorized"]:
            self.auth_error = True
            raise AuthError("Not authorized")
        if event.get("type") == "auth":
            return

        if self.message_handler:
            self.message_handler(message)

    def run_forever(self, *args, **kwargs):
        while True:
            if getattr(self, "auth_error", False):
                if self.auth_header not in dockercloud.api.http.invalid_auth_headers:
                    dockercloud.api.http.invalid_auth_headers.append(self.auth_header)
                raise AuthError("Not authorized")
            ws = websocket.WebSocketApp(self.url, header=self.header,
                                        on_open=self._on_open,
                                        on_message=self._on_message,
                                        on_error=self._on_error,
                                        on_close=self._on_close)
            ws.run_forever(ping_interval=10, ping_timeout=5, *args, **kwargs)
