from __future__ import absolute_import

from .base import Mutable


class Swarm(Mutable):
    subsystem = "infra"
    endpoint = "/swarm"
