from __future__ import absolute_import

from .base import Immutable


class AZ(Immutable):
    subsystem = "infra"
    endpoint = "/az"
    namespacable = False

    @classmethod
    def _pk_key(cls):
        return 'name'
