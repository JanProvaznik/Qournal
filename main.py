import sys, json
from model.Models import *

DEFAULT_PATH = ""
state = {}


def ListAreas(args):
    """Creates """
    pass


def AddArea(args):
    """Creates """

    pass


def RemoveArea(args):
    if not len(args) == 1:
        raise ArgumentError("Error: Name not specified")
    name = args[0]
    for area in state:
        if name == area.name:
            decision = input("Do you really want to delete the {name} area? Y/n 1/0")
            if decision in ["1", "Y", "y", "yes"]:
                del area
                return True
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


def SaveState(args=DEFAULT_PATH):
    """Puts the state of diary to JSON"""
    global state
    if not len(args) == 1:
        raise ArgumentError("Too many parameters")
    with open(args, "w+") as j:
        json.dump(state, j)


def RecoverState(args=DEFAULT_PATH):
    """Recovers the state of diary from JSON"""
    global state
    if not len(args) == 1:
        raise ArgumentError("Too many parameters")
    path = args
    try:
        with open(path, "r") as j:
            state = json.load(j)
    except FileNotFoundError:
        print("Error: Invalid path to JSON.")
    return
    pass


comms = {
    "listas": Command("listarea", "lists available areas", ListAreas),
    "adda": Command("addarea", "adds area and runs the change area subprogram", AddArea, ["name", "type"]),
    "rema": Command("removearea", "removes specified area", RemoveArea, ["name"]),
    "changea": Command("changearea", "runs the change area subprogram", ["name"]),
    "dispa": Command("displayarea", "displays specified area", DisplayArea, ["name"]),
    "addall": Command("adddaytoall", "runs the add day subprogram for all areas", AddDay),
    "addspec": Command("adddaytospecific", "runs the add day subprogram for specified area", AddDay, ["name"]),
    "commit": Command("commit", "commits data to json", SaveState, ["path"]),
    "recover": Command("recover", "recovers data from json", RecoverState, ["path"])

}


def mainLoop(path, commands):
    global state
    print("for the list of commands type 'help'")
    RecoverState(path)
    while True:
        command, *args = input().split()
        if command == "help":
            for c in commands:
                print(f"{c} args:{str(*c.args)} {c.description}")
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
