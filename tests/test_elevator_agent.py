#!/usr/bin/env python
# encoding: utf-8

import simpy
import unittest
from elevator_simulation.agents import Simulation, ElevatorBank, Building


class TestElevatorAgent(unittest.TestCase):
    """Test case docstring."""

    def setUp(self):
        self.sim = Simulation(number_of_floors=10)
        self.elevator_bank = ElevatorBank(self.sim, self.sim.building.floors)
        self.elevator = self.elevator_bank.add_elevator()

    def tearDown(self):
        pass

    # TODO: add a test for stopping at each floor

    def test_add_elevator_stop_top(self):
        travel_time = self.elevator.elevator_travel_secs
        total_run_time = travel_time * (len(self.elevator_bank.floors)) + self.elevator.elevator_open_secs
        num_tests = 1
        def test_floor(event):
            nonlocal num_tests
            now = self.sim.env.now
            expected_level = int(now / travel_time) + 1
            self.assertEqual(expected_level, self.elevator.location.level)
            num_tests += 1

        self.elevator.arrived_at_floor_event.callbacks.append(test_floor)
        self.elevator.add_stop(self.elevator_bank.floors[-1])
        self.sim.env.run(until=total_run_time)
        self.assertEqual(total_run_time, self.sim.env.now)
        self.assertEqual(num_tests, len(self.elevator_bank.floors))
        self.assertFalse(self.elevator.stops)
