#!/usr/bin/env python
# encoding: utf-8


import unittest
from datetime import timedelta
from elevator_simulation.models.building import Floor
from elevator_simulation.models.person import Schedule

class TestPerson(unittest.TestCase):
    """Test person behavior and functionality."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_name(self):
        pass


class TestSchedule(unittest.TestCase):
    """Test that the schedule can be properly manipulated"""

    def setUp(self):
        self.schedule = Schedule()
        self.floor = Floor(level=1)

    def tearDown(self):
        pass

    def test_add_event_bad_type(self):
        """tests that the right behavior occurs when adding an event with bad type."""
        with self.assertRaises(TypeError):
            self.schedule.add_event(12, self.floor)

    def test_add_event_bad_range(self):
        """tests that the right behavior occurs when adding an event with out of range time."""
        with self.assertRaises(ValueError):
            self.schedule.add_event(timedelta(days=2), self.floor)

        with self.assertRaises(ValueError):
            self.schedule.add_event(timedelta(days=1, microseconds=1), self.floor)

        with self.assertRaises(ValueError):
            self.schedule.add_event(timedelta(microseconds=-1), self.floor)

    def test_add_event_bad_location(self):
        """tests that the right behavior occurs when adding an event with bad location type."""
        with self.assertRaises(TypeError):
            self.schedule.add_event(timedelta(), None)

    def test_add_event(self):
        """tests that the right bheavior occurs when adding an event."""
        self.assertEqual(0, len(self.schedule.events))
        self.schedule.add_event(timedelta(hours=8, minutes=0), self.floor, "Go to work")
        self.assertEqual(1, len(self.schedule.events))
