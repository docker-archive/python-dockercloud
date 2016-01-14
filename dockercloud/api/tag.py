from __future__ import absolute_import

from .base import Taggable, BasicObject
from .exceptions import ApiError


class Tag(BasicObject):
    def __init__(self):
        self.tags = []

    def add(self, tagname):
        if isinstance(tagname, list):
            for t in tagname:
                self.taggable.tags.append({"name": t})
        else:
            self.taggable.tags.append({"name": tagname})

        self.taggable.__addchanges__('tags')

    @classmethod
    def create(cls, **kwargs):
        return cls(**kwargs)

    def remove(self, tagname):
        if not self.taggable:
            raise ApiError("You must initialize the tag object before performing this operation")

        _tags = []
        tagnames = []
        if isinstance(tagname, list):
            for n in tagname:
                tagnames.append(n)
        else:
            tagnames.append(tagname)

        for t in self.taggable.tags:
            for tagname in tagnames:
                if t.get("name", "") == tagname:
                    _tags.append(t)

        if _tags:
            for _tag in _tags:
                self.taggable.tags.remove(_tag)
            self.taggable.__addchanges__('tags')

    def delete(self, tagname):
        if not self.taggable:
            raise ApiError("You must initialize the tag object before performing this operation")

        if self.taggable.is_dirty:
            raise ApiError("You must save the tab object before performing this operation")

        self.remove(tagname)
        return self.save()

    @classmethod
    def fetch(cls, taggable):
        if not isinstance(taggable, Taggable):
            raise ApiError("The object does not support tag")
        if not taggable._detail_uri:
            raise ApiError("You must save the taggable object before performing this operation")

        tag = cls()
        tag.taggable = taggable

        return tag

    def list(self, **kwargs):
        if not self.taggable:
            raise ApiError("You must initialize the tag object before performing this operation")

        return self.taggable.tags

    def save(self):
        if not self.taggable:
            raise ApiError("You must initialize the tag object before performing this operation")

        return self.taggable.save()
