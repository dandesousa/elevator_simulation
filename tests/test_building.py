#!/usr/bin/env python
# encoding: utf-8

import unittest
from elevator_simulation.models.building import Building, Floor


class TestBuilding(unittest.TestCase):
    """Tests that building model works correctly"""

    def setUp(self):
        self.building = Building()

    def tearDown(self):
        pass

    def test_add_floors(self):
        """Tests that the floor is added to the building correctly
        and the level is updated in the floor regardless of what is passed"""
        self.assertEqual(0, len(self.building.floors))
        self.building.add_floor(Floor(level=10))
        self.building.add_floor(Floor(level=10))
        self.building.add_floor(Floor(level=10))
        self.assertEqual(3, len(self.building.floors))
        for i in range(len(self.building.floors)):
            self.assertEqual(i+1, self.building.floors[i].level)
