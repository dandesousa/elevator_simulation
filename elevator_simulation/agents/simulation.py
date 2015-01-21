#!/usr/bin/env python
# encoding: utf-8

import simpy
from elevator_simulation.agents.building import BuildingAgent
from elevator_simulation.agents.person import PersonAgent
from elevator_simulation.agents.elevator import ElevatorBankAgent


class Simulation(object):
    """Holds all of the objects in the simulation."""

    def __init__(self, building, people=[], elevator_banks=[], **kwargs):
        """Constructs a simulation from the models passed.

        :param building Building: the model of the building to run the simulation
        :param people list: list of the people in the simulation
        :param elevator_banks list: list of the elevator banks (controllers in the simulation
        """
        self.env = simpy.Environment()
        self.__building_model = building
        self.__building_agent = BuildingAgent(self, building)
        self.__person_models = people
        self.__person_agents = [PersonAgent(self, person) for person in people]
        self.__elevator_bank_models = elevator_banks
        self.__elevator_bank_agents = [ElevatorBankAgent(self, elevator_bank) for elevator_bank in elevator_banks]

    def run(self):
        self.env.run(until=24*3600)

    @property
    def building_agent(self):
        return self.__building_agent

    @property
    def person_agents(self):
        return self.__person_agents

    @property
    def elevator_bank_agents(self):
        return self.__elevator_bank_agents
