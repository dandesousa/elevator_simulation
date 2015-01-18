#!/usr/bin/env python
# encoding: utf-8

import simpy
import unittest
from elevator_simulation.models.building import Floor
from elevator_simulation.models.elevator import ElevatorController
from elevator_simulation.agents.elevator import ElevatorAgent


class TestElevatorAgent(unittest.TestCase):
    """Test case docstring."""

    def setUp(self):
        self.env = simpy.Environment()
        floors = []
        for i in range(10):
            floors.append(Floor(i+1))
        self.ctrl = ElevatorController(floors)
        self.first_elevator = self.ctrl.add_elevator()
        self.agent = ElevatorAgent(self.env, self.first_elevator)

    def tearDown(self):
        pass

    # TODO: add a test for stopping at each floor

    def test_add_elevator_stop_top(self):
        travel_time = self.agent.elevator_travel_secs
        total_run_time = travel_time * (len(self.ctrl.floors)) + self.agent.elevator_open_secs
        num_tests = 1
        def test_floor(event):
            nonlocal num_tests
            now = self.env.now
            expected_level = int(now / travel_time) + 1
            self.assertEqual(expected_level, self.agent.model.location.level)
            num_tests += 1

        self.agent.arrived_at_floor_event.callbacks.append(test_floor)
        self.agent.add_stop(self.ctrl.floors[-1])
        self.env.run(until=total_run_time)
        self.assertEqual(total_run_time, self.env.now)
        self.assertEqual(num_tests, len(self.ctrl.floors))
        self.assertFalse(self.agent.model.stops)
