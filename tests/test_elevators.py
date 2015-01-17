#!/usr/bin/env python
# encoding: utf-8

import unittest
from elevator_simulation.models.elevator import ElevatorController, Elevator
from elevator_simulation.models.building import Floor

class TestElevator(unittest.TestCase):
    """Tests various elevator function in the simulation."""

    def setUp(self):
        floors = []
        for i in range(10):
            floors.append(Floor(i+1))

        self.ctrl = ElevatorController()
        self.ctrl.add_elevator()
        self.ctrl.add_elevator()

    def tearDown(self):
        pass

    def test_add_elevator(self):
        """tests adding elevator logic"""
        self.assertEqual(2, len(self.ctrl.elevators))
        self.ctrl.add_elevator()
        self.assertEqual(3, len(self.ctrl.elevators))

    def test_name(self):
        pass
