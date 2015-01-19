#!/usr/bin/env python
# encoding: utf-8

import simpy
from elevator_simulation.models.building import Building


class BuildingAgent(object):
    def __init__(self, sim, model):
        self.env = sim.env
        self.model = model

        # TODO: create the buidling according to the specifications
        self.__elevator_available_events = [self.env.event() for floor in self.model.floors]

    def elevator_available_event(self, floor):
        return self.__elevator_available_events[floor.level]

    def reset_elevator_available_event(self, floor):
        self.__elevator_available_events[floor.level] = self.env.event()
