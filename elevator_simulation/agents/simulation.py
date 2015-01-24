#!/usr/bin/env python
# encoding: utf-8

import simpy
from elevator_simulation.agents import Building

class Simulation(object):
    """Holds all of the objects in the simulation."""

    EOD = 24*3600

    def __init__(self, **kwargs):
        """Constructs a simulation from the models passed.

        :param number_of_floors int: Number of floors in the building (def: 10)
        """
        self.__env = simpy.Environment()
        self.__building = Building(self, kwargs.get("number_of_floors", 10))
        self.__people = []
        self.__elevator_banks = []

    def __eq__(self, obj):
        return self.building == obj.building and self.people == obj.people and self.elevator_banks == obj.elevator_banks

    def run(self):
        self.env.run(until=Simulation.EOD)

    @property
    def env(self):
        return self.__env

    @property
    def building(self):
        return self.__building

    @property
    def people(self):
        return self.__people

    @property
    def elevator_banks(self):
        return self.__elevator_banks
