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
        self.assertEqual(bdata["floors"], len(self.simulation.building.floors))

    def test_elevator_banks(self):
        edata = self.data["elevator_banks"]
        self.assertEqual(len(edata), len(self.simulation.elevator_banks))
        # TODO: test strategy?
        for i in range(len(edata)):
            elevator_bank_data = edata[i]
            elevator_bank = self.simulation.elevator_banks[i]
            self.assertEqual(len(elevator_bank_data["elevators"]), len(elevator_bank.elevators))
            for i in range(len(elevator_bank_data["elevators"])):
                elevator_data = elevator_bank_data["elevators"][i]
                elevator = elevator_bank.elevators[i]
                if "capacity" in elevator_data:
                    self.assertEqual(elevator_data["capacity"], elevator.capacity)

    def test_people(self):
        # TODO test name
        pdata = self.data["people"]
        self.assertEqual(len(pdata), len(self.simulation.people))
        i = 0
        for person_data in pdata:
            person = self.simulation.people[i]
            # schedule test
            schedule_data = person_data["schedule"]
            for j in range(len(schedule_data)):
                event_data = schedule_data[j]
                event = person.schedule.events[j]
                self.assertEqual(event_data["start"], event.start_time.total_seconds())
                self.assertEqual(event_data["level"], event.location.level)
            i += 1
