from __future__ import absolute_import

from .base import Mutable, Taggable


class Repository(Mutable, Taggable):
    subsystem = "repo"
    endpoint = "/repository"

    @classmethod
    def _pk_key(cls):
        return 'name'
