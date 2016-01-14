from __future__ import absolute_import

from .base import Mutable, Taggable


class Node(Mutable, Taggable):
    subsystem = "infra"
    endpoint = "/node"

    def save(self):
        if not self._detail_uri:
            raise AttributeError("Adding a new node is not supported via 'save' method")
        super(Node, self).save()

    def deploy(self, tag=None):
        return self._perform_action("deploy")

    def upgrade_docker(self):
        return self._perform_action("docker-upgrade")
