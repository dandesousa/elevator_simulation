#!/usr/bin/env python
# encoding: utf-8

import json
import os
import unittest
from elevator_simulation.readers.json import read_simulation


class TestJSONReader(unittest.TestCase):
    """Tests that the json reader is able to read the json file correctly."""

    def setUp(self):
        test_data_path = os.path.join(os.path.dirname(__file__), "data")
        simple_test_file = os.path.join(test_data_path, "simple.json")
        self.simulation = read_simulation(simple_test_file)

        with open(simple_test_file, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def tearDown(self):
        pass

    def test_building_floors(self):
        bdata = self.data["building"]
        self.assertEqual(bdata["floors"], len(self.simulation.building_agent.model.floors))
