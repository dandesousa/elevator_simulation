#!/usr/bin/env python
# encoding: utf-8


class Floor(object):
    def __init__(self, name=None):
        self.__name = name
        self.__elevator_lobby = None
        self.__office_space = None
        self.__stair_well = None
        self.__lunch_room = None


class Building(object):
    def __init__(self):
        self.__floors = []

    @property
    def floors(self):
        """Gets a tuple of floors"""
        return tuple(self.__floors)

    def add_floor(self, floor):
        """Adds a floor to the building.

        :param floor Floor: floor to add

        >>> b = Building()
        >>> fl = Floor()
        >>> b.add_floor(fl)
        >>> fl in b.floors
        True
        """
        if not isinstance(floor, Floor):
            raise TypeError("Expected param floor to be of type {}".format(Floor.__name__))

        self.__floors.append(floor)
