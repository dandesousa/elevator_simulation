#!/usr/bin/env python
# encoding: utf-8


class Floor(object):
    """class representing a floor."""

    def __init__(self, level=None):
        """intializes a floor with a level label"""
        self._level = level

    @property
    def level(self):
        """integer identifier indicates the height of the floor relative to other floors"""
        return self._level

    def direction(self, fl):
        """the direction you must travel to from this floor to the passed floor

        :param fl Floor: the floor to return the direction towards.
        """
        return (fl.level - self.level) / self.distance(fl)

    def distance(self, fl):
        """computes the distance between two floors based on the level

        :param fl Floor: the floor to calculate the distance between."""
        return abs(self.level - fl.level)

    def __repr__(self):
        return "Floor({})".format(self.level)


class Building(object):
    """Class which models the building used in the simulation."""

    def __init__(self):
        """intializes a building with an empty set of floors"""
        self.__floors = tuple()

    @property
    def floors(self):
        """Gets a tuple of floors"""
        return self.__floors

    def add_floor(self, floor=None):
        """Adds a floor to the building.

        :param floor Floor: floor to add

        >>> b = Building()
        >>> fl = Floor()
        >>> b.add_floor(fl)
        >>> fl in b.floors
        True
        """
        if floor is None:
            floor = Floor()

        if not isinstance(floor, Floor):
            raise TypeError("Expected param floor to be of type {}".format(Floor.__name__))

        self.__floors += (floor, )
        floor._level = len(self.__floors)
