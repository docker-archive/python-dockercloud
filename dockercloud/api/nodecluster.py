from __future__ import absolute_import

from .base import Mutable, Taggable
from .noderegion import Region
from .nodetype import NodeType


class NodeCluster(Mutable, Taggable):
    subsystem = "infra"
    endpoint = "/nodecluster"

    def deploy(self, tag=None):
        return self._perform_action("deploy")

    @classmethod
    def create(cls, **kwargs):
        for key, value in kwargs.items():
            if key == "node_type" and isinstance(value, NodeType):
                kwargs[key] = getattr(value, "resource_uri", "")
            if key == "region" and isinstance(value, Region):
                kwargs[key] = getattr(value, "resource_uri", "")
        return cls(**kwargs)
