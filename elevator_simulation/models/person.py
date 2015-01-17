#!/usr/bin/env python
# encoding: utf-8


class Schedule(object):
    def __init__(self):
        self.__events = []

    def add_event(self, start_time, end_time, location):
        self.__events.append((start_time, end_time, location))


class Person(object):
    def __init__(self):
        self.__schedule = Schedule()
        self.__location = None

    @property
    def schedule(self):
        return self.__schedule

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, value):
        # TODO: set location type, like None or Floor
        self.__location = value
