#!/usr/bin/env python
# encoding: utf-8

from elevator_simulation.agents import AgentMixin
from elevator_simulation.models import Building as BuildingModel


class Building(AgentMixin, BuildingModel):
    def __init__(self, sim, num_floors):
        AgentMixin.__init__(self, sim)
        BuildingModel.__init__(self)

        for i in range(num_floors):
            self.add_floor()

        # TODO: create the buidling according to the specifications
        self.__elevator_available_events = [self.env.event() for floor in self.floors]

    def elevator_available_event(self, floor):
        return self.__elevator_available_events[floor.level-1]

    def reset_elevator_available_event(self, floor):
        event = self.env.event()
        event.callbacks = self.elevator_available_event(floor).callbacks
        self.__elevator_available_events[floor.level-1] = self.env.event()
