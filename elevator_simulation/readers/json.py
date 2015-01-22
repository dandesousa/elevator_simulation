#!/usr/bin/env python
# encoding: utf-8


import json
from datetime import timedelta
from elevator_simulation.agents import ElevatorBank, Person, Simulation


def read_simulation(filename):
    """Reads a json file for simulation settings

    :filename: TODO
    :returns: TODO
    """
    simulation = None
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

        # create the buidling according to specifications
        if "building" not in data:
            raise ValueError("Expected 'building' element in file")

        building_data = data["building"]
        num_floors = building_data["floors"]
        simulation = Simulation(number_of_floors=num_floors)

        if "elevator_banks" not in data:
            raise ValueError("Expected 'elevator_banks' element in file")

        elevator_data = data["elevator_banks"]
        for elevator_bank in elevator_data:
            ctrl = ElevatorBank(simulation, simulation.building.floors)  # TODO: read the strategy optionally?
            elevator_arg_list = elevator_bank["elevators"]
            for elevator_args in elevator_arg_list:
                ctrl.add_elevator(**elevator_args)
            simulation.elevator_banks.append(ctrl)

        # create the people according to person/schedule specifications
        people_data = data["people"]
        for person_data in people_data:
            person = Person(simulation, **person_data)
            schedule_data = person_data["schedule"]
            for event_data in schedule_data:
                start_time = timedelta(seconds=event_data["start"])
                location = simulation.building.floors[event_data["level"]-1]
                description = event_data.get("description", "unknown")
                person.schedule.add_event(start_time, location, description)
            simulation.people.append(person)

    return simulation
