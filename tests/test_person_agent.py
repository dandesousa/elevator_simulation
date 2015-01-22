#!/usr/bin/env python
# encoding: utf-8

import logging
import unittest
from elevator_simulation.agents import Person, Simulation, ElevatorBank
from datetime import timedelta


class TestElevatorAgent(unittest.TestCase):
    """Test case docstring."""

    def setUp(self):
        logging.basicConfig(format="%(levelname)s %(asctime)s: %(message)s", level=logging.DEBUG)
        self.sim = Simulation(number_of_floors=10)
        self.ctrl = ElevatorBank(self.sim, self.sim.building.floors)
        self.first_elevator = self.ctrl.add_elevator()
        self.sim.elevator_banks.append(self.ctrl)
        self.person = Person(self.sim)
        self.person.schedule.add_event(timedelta(hours=7),  self.sim.building.floors[6])
        self.person.schedule.add_event(timedelta(hours=12), self.sim.building.floors[5])
        self.person.schedule.add_event(timedelta(hours=16), self.sim.building.floors[0])
        self.sim.people.append(self.person)

    def tearDown(self):
        pass

    def test_arrives_at_work_level(self):
        until_time = timedelta(hours=8).total_seconds()
        self.sim.env.run(until=until_time)
        self.assertEqual(self.person.location, self.person.schedule.events[0].location)
