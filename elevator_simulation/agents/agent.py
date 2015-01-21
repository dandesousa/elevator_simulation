#!/usr/bin/env python
# encoding: utf-8


class AgentMixin(object):
    """Base class defining agents """
    def __init__(self, simulation, model):
        self.__simulation = simulation
        self.__env = simulation.env
        self.__model = model

    @property
    def simulation(self):
        return self.__simulation

    @property
    def env(self):
        return self.__env

    @property
    def model(self):
        return self.__model
