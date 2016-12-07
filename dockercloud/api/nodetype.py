from __future__ import absolute_import

from .base import Immutable


class NodeType(Immutable):
    subsystem = "infra"
    endpoint = "/nodetype"
    is_namespaced = False

    @classmethod
    def _pk_key(cls):
        return 'name'
