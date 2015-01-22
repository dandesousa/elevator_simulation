#!/usr/bin/env python
# encoding: utf-8


class AgentMixin(object):
    """Mixin class defining agents of a simpy simulation."""

    def __init__(self, simulation):
        self.__simulation = simulation

    @property
    def simulation(self):
        """the simulation object that this agent lives under"""
        return self.__simulation

    @property
    def env(self):
        """the simpy environment under which the simulation is running"""
        return self.__simulation.env
