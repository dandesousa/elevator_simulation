#!/usr/bin/env python
# encoding: utf-8

import simpy
from datetime import timedelta
from elevator_simulation.models.person import Person

class PersonAgent(object):
    """Behavior for person agent"""
    def __init__(self, env, **kwargs):
        self.env = env
        self.model = Person()
        self.action = env.process(self.run())

    def run(self):
        while True:
            now_td = timedelta(self.env.now)
            next_event = self.model.schedule.next_event(now_td)
            time_until_next_event = next_event.start_time - now_td
            # waits until the next event time
            yield self.env.timeout(time_until_next_event.total_seconds())

            distance = self.model.location.distance(next_event.location)
            direction = self.model.location.direction(next_event.location)
            # TODO: correct later to check for stairs
            # determine whether to take the steps or call the elevator
            # if elevator, call elevator and wait
            elevator_agent = self.elevator_controller_agent.call(next_event, direction)

            # when elevator arrives, add stop
            # when elevator arrives at stop, update location

    def call_and_wait_for_elevator(self):
        self.elevator_controller_agent.call(sel
