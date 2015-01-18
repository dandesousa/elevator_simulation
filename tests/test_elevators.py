#!/usr/bin/env python
# encoding: utf-8

import unittest
from elevator_simulation.models.elevator import ElevatorController, Elevator
from elevator_simulation.models.building import Floor

class TestElevatorController(unittest.TestCase):
    """Tests various elevator controller function in the simulation."""

    def setUp(self):
        floors = []
        for i in range(10):
            floors.append(Floor(i+1))

        self.ctrl = ElevatorController(floors)
        self.ctrl.add_elevator()
        self.ctrl.add_elevator()

    def tearDown(self):
        pass

    def test_add_elevator(self):
        """tests adding elevator logic"""
        self.assertEqual(2, len(self.ctrl.elevators))
        self.ctrl.add_elevator()
        self.assertEqual(3, len(self.ctrl.elevators))

    def test_(self):
        pass


class TestElevator(unittest.TestCase):
    """Tests various elevator functions in the simulation."""

    def setUp(self):
        floors = []
        for i in range(10):
            floors.append(Floor(i+1))

        self.ctrl = ElevatorController(floors)
        self.ctrl.add_elevator()
        self.elevator = self.ctrl.elevators[0]

    def tearDown(self):
        pass

    def test_distance(self):
        """tests that the distance between elevator and various levels is correct"""
        for floor in self.ctrl.floors:
            self.assertEqual(floor.level - 1, self.elevator.distance(floor))

    def test_direction(self):
        """tests the valid values that are applicable for a direction"""
        self.assertFalse(self.elevator.direction)

        valid_values = (1, -1, 0, None)
        for value in valid_values:
            self.elevator.direction = value
            self.assertEqual(value, self.elevator.direction)

        with self.assertRaises(ValueError):
            self.elevator.direction = 2

    def test_moving_away(self):
        """tests that we can properly determine if we are moving away"""
        for floor in self.ctrl.floors:
            self.assertFalse(self.elevator.moving_away(floor))
        self.elevator.direction = 1

        floors = []
        while self.elevator.location != self.ctrl.floors[-1]:
            for floor in floors:
                self.assertTrue(self.elevator.moving_away(floor))
            floors.append(self.elevator.location)
            self.elevator.location = self.elevator.next_location


    def test_next_location(self):
        """tests that the next location is selected accurately given a direction and current location"""
        self.assertEqual(self.ctrl.floors[0], self.elevator.location)
        self.assertEqual(self.elevator.location, self.elevator.next_location)

        self.elevator.direction = -1
        self.assertEqual(self.elevator.location, self.elevator.next_location)

        self.elevator.direction = 0
        self.assertEqual(self.elevator.location, self.elevator.next_location)

        self.elevator.direction = 1
        while self.elevator.location != self.ctrl.floors[-1]:
            self.assertEqual(self.ctrl.floors[self.elevator.location.level], self.elevator.next_location)
            self.elevator.location = self.elevator.next_location
        self.assertEqual(self.ctrl.floors[-1], self.elevator.next_location)
        self.assertEqual(self.elevator.location, self.elevator.next_location)

        self.elevator.direction = -1
        while self.elevator.location != self.ctrl.floors[0]:
            self.assertEqual(self.ctrl.floors[self.elevator.location.level-2], self.elevator.next_location)
            self.elevator.location = self.elevator.next_location
        self.assertEqual(self.ctrl.floors[0], self.elevator.next_location)
        self.assertEqual(self.elevator.location, self.elevator.next_location)
