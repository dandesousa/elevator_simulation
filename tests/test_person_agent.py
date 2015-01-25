#!/usr/bin/env python
# encoding: utf-8

import logging
import unittest
from elevator_simulation.agents import Person, Simulation, ElevatorBank
from datetime import timedelta


class TestPersonAgent(unittest.TestCase):
    """Test case docstring."""

    def setUp(self):
        logging.basicConfig(format="%(levelname)s %(asctime)s: %(message)s", level=logging.DEBUG)
        self.sim = Simulation(number_of_floors=10)
        self.ctrl = ElevatorBank(self.sim)
        self.first_elevator = self.ctrl.add_elevator(capacity=1)
        self.sim.elevator_banks.append(self.ctrl)
        self.person = Person(self.sim)
        self.person.schedule.add_event(timedelta(hours=7),  self.sim.building.floors[6])
        self.person.schedule.add_event(timedelta(hours=12), self.sim.building.floors[5])
        self.person.schedule.add_event(timedelta(hours=16), self.sim.building.floors[0])
        self.sim.people.append(self.person)

    def tearDown(self):
        pass

    def test_elevator_capacity_skip(self):
        """tests that we don't enter the elevator if the capacity is full"""
        person2 = Person(self.sim)
        person2.schedule.add_event(timedelta(hours=7),  self.sim.building.floors[3])
        self.sim.people.append(person2)
        num_tests = 1
        def count_floor(event):
            nonlocal num_tests
            num_tests += 1
        person2.register_event_callback("floor_reached", count_floor)
        until_time = timedelta(hours=8).total_seconds()
        self.sim.env.run(until=until_time)
        self.assertEqual(4, num_tests)

    def test_arrives_at_work_level(self):
        """tests that we arrive at the work level"""
        until_time = timedelta(hours=8).total_seconds()
        self.sim.env.run(until=until_time)
        self.assertEqual(self.first_elevator.location, self.person.schedule.events[0].location)
        self.assertEqual(self.person.location, self.person.schedule.events[0].location)

    def test_arrives_at_lunch_level(self):
        until_time = timedelta(hours=13).total_seconds()
        self.sim.env.run(until=until_time)
        self.assertEqual(self.first_elevator.location, self.person.schedule.events[1].location)
        self.assertEqual(self.person.location, self.person.schedule.events[1].location)

    def test_arrives_work_done_level(self):
        until_time = timedelta(hours=17).total_seconds()
        self.sim.env.run(until=until_time)
        self.assertEqual(self.first_elevator.location, self.person.schedule.events[2].location)
        self.assertEqual(self.person.location, self.person.schedule.events[2].location)
