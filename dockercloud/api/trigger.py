import json as json_parser

from .base import Triggerable, BasicObject
from .exceptions import ApiError
from .http import send_request


class Trigger(BasicObject):
    def __init__(self):
        self.trigger = None

    def add(self, name=None, operation=None):

        if self.trigger is not None:
            raise ApiError("You must save the object before performing this operation")

        trigger = {}
        if name:
            trigger['name'] = name
        if operation:
            trigger['operation'] = operation
        self.trigger = trigger

    @classmethod
    def create(cls, **kwargs):
        """Returns a new instance of the model (without saving it) with the attributes specified in ``kwargs``

        :returns: trigger -- a new local instance of the Trigger
        """
        return cls(**kwargs)

    def delete(self, uuid):
        if not self.endpoint:
            raise ApiError("You must initialize the Trigger object before performing this operation")

        action = "DELETE"
        url = "/".join([self.endpoint, uuid])
        send_request(action, url)
        return True

    @classmethod
    def fetch(cls, triggerable):
        if not isinstance(triggerable, Triggerable):
            raise ApiError("The object does not support trigger")

        if not triggerable._detail_uri:
            raise ApiError("You must save the triggerable object before performing this operation")

        trigger = cls()
        trigger.endpoint = "/".join([triggerable._detail_uri, "trigger"])
        handlers = []
        for t in trigger.list():
            triggername = t.get("name", "")
            if triggername:
                handlers.append({"name": triggername})
        return trigger

    def list(self, **kwargs):
        if not self.endpoint:
            raise ApiError("You must initialize the Trigger object before performing this operation")

        objects = []
        while True:
            json = send_request('GET', self.endpoint, params=kwargs)
            objs = json.get('objects', [])
            meta = json.get('meta', {})
            next_url = meta.get('next', '')
            offset = meta.get('offset', 0)
            limit = meta.get('limit', 0)
            objects.extend(objs)
            if next_url:
                kwargs['offset'] = offset + limit
                kwargs['limit'] = limit
            else:
                break

        return objects

    def save(self):
        if not self.endpoint:
            raise ApiError("You must initialize the Trigger object before performing this operation")

        if self.trigger is None:
            return True

        json = send_request("POST", self.endpoint, data=json_parser.dumps(self.trigger))
        if json:
            self.clear()
            self.clear()
            return True

    def call(self, uuid):
        if not self.endpoint:
            raise ApiError("You must initialize the Trigger object before performing this operation")

        json = send_request("POST", "/".join([self.endpoint, uuid + "/call"]))
        if json:
            return True
        return False

    def clear(self):
        self.trigger = None
