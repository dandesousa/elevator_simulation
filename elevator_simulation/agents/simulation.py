#!/usr/bin/env python
# encoding: utf-8


from elevator_simulation.agents.building import BuildingAgent
from elevator_simulation.agents.person import PersonAgent
from elevator_simulation.agents.elevator import ElevatorControllerAgent

class Simulation(object):
    """Holds all of the objects in the simulation."""

    def __init__(self):
        self.__building = BuildingAgent()
        self.__people = []
        self.__elevator_banks = []

    @property
    def building(self):
        return self.__building

    @property
    def people(self):
        return self.__people

    @property
    def elevator_banks(self):
        return self.__elevator_banks
