#!/usr/bin/env python
# encoding: utf-8


class AgentMixin(object):
    """Mixin class defining agents of a simpy simulation."""

    def __init__(self, simulation, events=[]):
        self.__simulation = simulation
        self.__event_callbacks = {event: [] for event in events}
        self.__events = {event: self.env.event() for event in events}

    @property
    def simulation(self):
        """the simulation object that this agent lives under"""
        return self.__simulation

    @property
    def env(self):
        """the simpy environment under which the simulation is running"""
        return self.__simulation.env

    def event(self, event_name):
        """returns the events with the given name"""
        if event_name not in self.__events:
            raise ValueError("No event '{}' exists for this agent".format(event_name))

        return self.__events[event_name]

    def register_event_callback(self, event_name, callback):
        """registers an event callback for the given event

        :param event_name str: Name of the event
        :param callback function: The function to invoke as a callback.
        """
        if event_name not in self.__events:
            raise ValueError("No event '{}' exists for this agent".format(event_name))

        # appends to the callbacks
        self.__events[event_name].callbacks.append(callback)

        # saves for later
        self.__event_callbacks[event_name].append(callback)

    def notify_event(self, event_name, value=None):
        """triggers the event owned by this event with the given event name

        :param event_name str: name of the event to notify
        """
        if event_name not in self.__events:
            raise ValueError("No event '{}' exists for this agent".format(event_name))

        event = self.__events[event_name]
        self.__events[event_name] = self.env.event()
        for cb in self.__event_callbacks[event_name]:
            self.__events[event_name].callbacks.append(cb)
        event.succeed(value)
