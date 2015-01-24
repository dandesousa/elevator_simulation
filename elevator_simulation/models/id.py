#!/usr/bin/env python
# encoding: utf-8


import uuid


class IdentMixin(object):
    def __init__(self, **kwargs):
        self.__uuid = uuid.UUID(kwargs.get("uuid", uuid.uuid4().hex))

    @property
    def uuid(self):
        return self.__uuid.hex

    def __hash__(self):
        return self.__uuid.int

    def __eq__(self, obj):
        return self.__uuid == obj.__uuid
