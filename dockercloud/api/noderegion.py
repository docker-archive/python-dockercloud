from __future__ import absolute_import

from .base import Immutable


class Region(Immutable):
    subsystem = "infra"
    endpoint = "/region"

    @classmethod
    def _pk_key(cls):
        return 'name'
