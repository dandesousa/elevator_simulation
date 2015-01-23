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
