#!/usr/bin/env python
# encoding: utf-8

import simpy
import unittest
from datetime import timedelta
from elevator_simulation.agents import Simulation, ElevatorBank, Building, Person


class TestElevatorAgent(unittest.TestCase):
    """Test case docstring."""

    def setUp(self):
        self.sim = Simulation(number_of_floors=10)
        self.elevator_bank = ElevatorBank(self.sim)
        self.sim.elevator_banks.append(self.elevator_bank)
        self.elevator = self.elevator_bank.add_elevator()

    def tearDown(self):
        pass

    # TODO: add a test for stopping at each floor
    def test_elevator_idle(self):
        """tests that elevator stays where it is, when it has no stops"""
        self.assertEqual(1, self.elevator.location.level)
        self.sim.env.run(until=10000)
        self.assertEqual(1, self.elevator.location.level)
        self.elevator.add_stop(self.sim.building.floors[3])
        self.sim.env.run(until=20000)
        self.assertEqual(4, self.elevator.location.level)
        self.sim.env.run(until=30000)
        self.assertEqual(4, self.elevator.location.level)
        self.elevator.add_stop(self.sim.building.floors[7])
        self.sim.env.run(until=35000)
        self.assertEqual(8, self.elevator.location.level)
        self.sim.env.run(until=55000)
        self.assertEqual(8, self.elevator.location.level)

    def test_enter_exit_elevator(self):
        person = Person(self.sim)
        with self.assertRaises(RuntimeError):
            self.elevator.enter(person)

        self.elevator.open_doors()
        self.assertTrue(self.elevator.is_open)
        self.elevator.enter(person)
        self.assertIn(person, self.elevator)
        self.elevator.close_doors()
        self.assertFalse(self.elevator.is_open)

        with self.assertRaises(RuntimeError):
            self.elevator.exit(person)

        self.elevator.open_doors()
        self.elevator.exit(person)
        self.assertNotIn(person, self.elevator)

    def test_add_elevator_stop_top(self):
        travel_time = self.elevator.elevator_travel_secs
        total_run_time = travel_time * (len(self.elevator_bank.floors)) + self.elevator.elevator_open_secs
        num_tests = 1
        def test_floor(event):
            nonlocal num_tests
            now = self.sim.env.now
            expected_level = int((now - self.elevator.elevator_open_secs - self.elevator.elevator_close_secs - self.elevator.elevator_wait_secs) / travel_time) + 1
            self.assertEqual(expected_level, self.elevator.location.level)
            num_tests += 1

        person = Person(self.sim)
        person.schedule.add_event(timedelta(seconds=0), self.elevator_bank.floors[-1])
        person.register_event_callback("floor_reached", test_floor)
        self.sim.run()
        self.assertEqual(num_tests, len(self.elevator_bank.floors))
        self.assertFalse(self.elevator.stops)
