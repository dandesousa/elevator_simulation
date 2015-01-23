#!/usr/bin/env python
# encoding: utf-8


import unittest
from elevator_simulation.agents import AgentMixin
from elevator_simulation.agents import Simulation


class TestAgentMixin(unittest.TestCase):
    """Tests agent mixin functionality"""

    def setUp(self):
        self.sim = Simulation(number_of_floors=10)
        self.agent = AgentMixin(self.sim, events=["event1", "event2"])

    def tearDown(self):
        pass

    def test_event_bad_name(self):
        with self.assertRaises(ValueError):
            self.agent.register_event_callback("fakename", lambda v: v)

        with self.assertRaises(ValueError):
            self.agent.register_event_callback("fakename", lambda v: v)

    def test_event_register_callback(self):
        invoked = False
        def cb(value):
            nonlocal invoked
            invoked = True

        self.agent.register_event_callback("event2", cb)
        self.agent.notify_event("event1")
        self.sim.env.run(until=1)
        self.assertFalse(invoked)

        self.agent.notify_event("event2")
        self.sim.env.run(until=2)
        self.assertTrue(invoked)
