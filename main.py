import sys
import json,jsons
from model.Models import *

DEFAULT_PATH = ""
state = {}


def ListAreas(args):
    """ """
    for a in state.keys():
        print(a)


def AddArea(args):
    """Creates """
    if not len(args)==2:
        raise ArgumentError("Error: 2 arguments required: name and type")
    name = args[0]
    typestr = args[1]
    typeint = 0
    if typestr in ['1', 'checklist', 'cl']:
        typeint = 1
    if typestr in ['2', 'semanticData', 'semanticdata', 'semantic_data', 'sd']:
        typeint = 2
    if typestr in ['3', 'freetext', 'ft']:
        typeint = 3

    newa = Area(name, typeint,{})
    state[name] = newa
    print(f"Created area {name} of type {typestr}. Executing change area subprogram.")
    ChangeArea([name])


def RemoveArea(args):
    if not len(args) == 1:
        raise ArgumentError("Error: Name not specified")
    name = args[0]
    if name in state:
        decision = input("Do you really want to delete the {name} area? Y/n 1/0")
        if decision in ["1", "Y", "y", "yes"]:
            del state[name]
            return True
        return False
    else:
        raise ArgumentError("Error: Name of area not found.")


def ChangeArea(args):
    pass


def DisplayArea(args):
    pass


def AddDay():
    pass


def AddDayToArea(args):
    """Adds day to specified area.
    first arg, which day,
    """
    pass


def SaveState(args=tuple(DEFAULT_PATH)):
    """Puts the state of diary to JSON"""
    global state
    if not len(args) == 1:
        raise ArgumentError("Too many arguments.")
    with open(args[0], "w+") as j:
        j.write(str(jsons.dump(state)))


def RecoverState(args=DEFAULT_PATH):
    """Recovers the state of diary from JSON"""
    global state
    if not len(args) == 1:
        raise ArgumentError("Too many parameters")
    path = args[0]
    try:
        with open(path, "r") as j:
            state = jsons.load(j)
    except FileNotFoundError:
        print("Error: Invalid path to JSON.")


# basic commands definitions
comms = {
    "listas": Command("listarea", "lists available areas", ListAreas),
    "adda": Command("addarea", "adds area and runs the change area subprogram", AddArea, ["name", "type"]),
    "rema": Command("removearea", "removes specified area", RemoveArea, ["name"]),
    "changea": Command("changearea", "runs the change area subprogram", ChangeArea, ["name"]),
    "dispa": Command("displayarea", "displays specified area", DisplayArea, ["name"]),
    "addall": Command("adddaytoall", "runs the add day subprogram for all areas", AddDay),
    "addspec": Command("adddaytospecific", "runs the add day subprogram for specified area", AddDay, ["name"]),
    "commit": Command("commit", "commits data to json", SaveState, ["path"]),
    "recover": Command("recover", "recovers data from json", RecoverState, ["path"])

}


def mainLoop(path, commands):
    global state
    print("for the list of commands type 'help'")
    RecoverState([path])
    while True:
        command, *args = input().split()
        if command == "help":
            for c in commands.items():
                print(f"{c[0]} args:{str(*c[1].args)} {c[1].description}")

        elif command == "exit":
            print("Bye")
            sys.exit()
        else:
            if command in commands:
                try:
                    commands[command].function(args)
                except ArgumentError as e:
                    print(e.strerror)

            else:
                print("no such command")


mainLoop(DEFAULT_PATH, comms)
