#!/usr/bin/env python
# encoding: utf-8
import logging
import simpy
import unittest
from elevator_simulation.models.building import Building
from elevator_simulation.models.elevator import ElevatorBank
from elevator_simulation.models.person import Person
from elevator_simulation.agents.simulation import Simulation
from datetime import timedelta

class TestElevatorAgent(unittest.TestCase):
    """Test case docstring."""

    def setUp(self):
        logging.basicConfig(format="%(levelname)s %(asctime)s: %(message)s", level=logging.DEBUG)
        building = Building()
        for i in range(10):
            building.add_floor()
        self.ctrl = ElevatorBank(building.floors)
        self.first_elevator = self.ctrl.add_elevator()
        self.person = Person()
        self.person.schedule.add_event(timedelta(hours=7), building.floors[6])
        self.person.schedule.add_event(timedelta(hours=12), building.floors[5])
        self.person.schedule.add_event(timedelta(hours=16), building.floors[0])

        self.sim = Simulation(building, [self.person], [self.ctrl])
        self.env = self.sim.env
        self.elevator_agent = self.sim.elevator_bank_agents[0].elevator_agents[0]

    def tearDown(self):
        pass

    def test_arrives_at_work_level(self):
        until_time = timedelta(hours=8).total_seconds()
        self.sim.env.run(until=until_time)
        self.assertEqual(self.person.location, self.person.schedule.events[0].location)
