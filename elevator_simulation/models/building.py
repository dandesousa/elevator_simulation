#!/usr/bin/env python
# encoding: utf-8


class Floor(object):
    def __init__(self, level=None):
        self._level = level
        # TODO: remove these totall un-needed properties
        self.__elevator_lobby = None
        self.__office_space = None
        self.__stair_well = None
        self.__lunch_room = None

    @property
    def level(self):
        return self._level

    def direction(self, fl):
        """the direction you must travel to from this floor to the passed floor"""
        return (fl.level - self.level) / self.distance(fl)

    def distance(self, fl):
        """computes the distance between two floors based on the level"""
        return abs(self.level - fl.level)

    def __repr__(self):
        return "<Floor(level={})>".format(self.level)


class Building(object):
    """Class which models the building used in the simulation.

    TODO: adding this here at first but might not matter later
    """
    def __init__(self):
        self.__floors = tuple()

    @property
    def floors(self):
        """Gets a tuple of floors"""
        return self.__floors

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

        self.__floors += (floor, )
        floor._level = len(self.__floors)
