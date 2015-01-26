#!/usr/bin/env python
# encoding: utf-8


import json


def write_simulation(simulation, fh):
    """Writes a simulation to an output stream
    """
    data = dict()
    data["building"] = dict()
    data["building"]["floors"] = len(simulation.building.floors)

    data["elevator_banks"] = []
    for elevator_bank in simulation.elevator_banks:
        elb_dict = dict()
        data["elevator_banks"].append(elb_dict)
        elb_dict["elevators"] = []
        elb_dict["uuid"] = elevator_bank.uuid
        for elevator in elevator_bank.elevators:
            el_dict = dict()
            elb_dict["elevators"].append(el_dict)
            el_dict["uuid"] = elevator.uuid
            el_dict["capacity"] = elevator.capacity
            # TODO: rest of the attributes of elevator

    data["people"] = []
    for person in simulation.people:
        person_dict = dict()
        data["people"].append(person_dict)
        person_dict["uuid"] = person.uuid
        person_dict["elevator_call_strategy"] = person.call_strategy.__name__
        person_dict["schedule"] = []
        for event in person.schedule.events:
            event_dict = dict()
            person_dict["schedule"].append(event_dict)
            event_dict["start"] = event.start_time.total_seconds()
            event_dict["level"] = event.location.level
            event_dict["description"] = event.description

    json.dump(data, fh)
