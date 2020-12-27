import jsonpickle
import sys
from model.Models import *

DEFAULT_PATH = ""
state = {}


def ListAreas(args):
    """no args, just lists areas """
    for a in state.keys():
        print(a)


def AddArea(args):
    """Creates an area and then runs the change are subprogram"""
    if not len(args) == 2:
        raise ArgumentError("Error: 2 arguments required: name and type")
    name = args[0]
    area_type_str = args[1]
    area_type = 0
    if area_type_str in ['1', 'checklist', 'cl']:
        area_type = AreaTypes.CHECKLIST
    if area_type_str in ['2', 'semanticData', 'semanticdata', 'semantic_data', 'sd']:
        area_type = AreaTypes.SEMANTIC_DATA
    if area_type_str in ['3', 'freetext', 'ft']:
        area_type = AreaTypes.FREE_TEXT
    else:
        raise ArgumentError("Wrong type of area.")
    new_area = Area(name, area_type, {}, {})
    state[name] = new_area
    print(f"Created area {name} of type {area_type_str}. Executing change area subprogram.")
    ChangeArea([name])


def RemoveArea(args):
    if not len(args) == 1:
        raise ArgumentError("Error: Name not specified")
    name = args[0]
    if name in state:
        decision = input(f"Do you really want to delete the {name} area? Y/n 1/0")
        if decision in ["1", "Y", "y", "yes"]:
            del state[name]
            return True
        return False
    else:
        raise ArgumentError("Error: Name of area not found.")


def ChangeArea(args):
    """first arg[0] := name"""
    global state
    # error handling

    if len(args) != 1:
        raise ArgumentError("Wrong number of parameters. Expected 1.")
    area_name = args[0]
    if area_name not in state:
        raise ArgumentError(f"No area of name {area_name}")

    area = state[area_name]

    def ChangeItemTemplate(template):
        new_name = input(f"Enter new name for {template.name} (or press enter)")
        new_question = input("Enter new question (or press enter)")
        is_enabled = input("Enable this area? Y/N") in ['y', 'Y', '1', 'yes', 'Yes', ""]
        if len(new_question) == 0: new_question = template.meta["question"]
        if len(new_name) > 0:
            old_name = template.meta['name']
            old_template = area.item_templates.pop(old_name)
            old_template.name = new_name
            area.item_templates[new_name] = old_template

            # rename all items inside days in this area
            for day in area.days:
                if old_name in day.items:
                    day.items[new_name] = day.items.pop(old_name)
        else:
            new_name = template.name
            area.item_templates[new_name].meta["question"] = new_question
            area.item_templates[new_name].meta["enabled"] = is_enabled

    def AddItemTemplate():
        new_template_name = input("Enter name for Item template")
        new_template_question = input("Enter question for this item.")
        new_template = ItemTemplate(new_template_name, {"question": new_template_question, "enabled": True})
        area.item_templates[new_template_name] = new_template

    templates = area.item_templates
    if area.type == AreaTypes.CHECKLIST or area.type == AreaTypes.SEMANTIC_DATA:
        print(f"There currently these item templates: {' '.join(templates)}")
        while True:
            comm, *item_args = input("Enter command: addi to add an item template,"
                                     " chai <name> to change an item template,"
                                     " exit to exit the change area subprogram.").split()
            if comm == "addi" and len(item_args == 0):
                AddItemTemplate()
            elif comm == "chai" and len(item_args == 1):
                ChangeItemTemplate(templates[item_args[0]])
            elif comm == "exit":
                return True
            else:
                print("No such command. Try again.")

    elif area.type == AreaTypes.FREE_TEXT:
        if not templates:
            AddItemTemplate()
        else:
            ChangeItemTemplate(list(templates.values())[0])
    else:
        raise ValueError


def DisplayArea(args):
    """Displays area depending on its type. args[0]:=name of area
    possible upgrade: only selected date range"""
    global state
    if len(args) != 1:
        raise ArgumentError("Wrong number of parameters. Expected 1.")
    area_name = args[0]
    if area_name not in state:
        raise ArgumentError(f"No area of name {area_name}")
    area = state[area_name]
    if area.type == AreaTypes.CHECKLIST:
        # todo pretty print
        print()

    elif area.type == AreaTypes.SEMANTIC_DATA:
        # todo pretty print
        pass

    elif area.type == AreaTypes.FREE_TEXT:
        print(area.name)
        for day in area.days.values():
            print(f"{day.date}: {list(day.items.values())[0].data}")
            print()


def AddDay(args):
    # TODO error handling
    pass


def AddDayToArea(args):
    """Adds day to specified area.
    first arg, which day,
    """
    pass


def SaveState(args=[DEFAULT_PATH]):
    """Puts the state of diary to JSON"""
    global state
    if not len(args) == 1:
        raise ArgumentError("Too many arguments.")
    with open(args[0], "w+", encoding="UTF-8") as j:
        encoded_state = jsonpickle.encode(state, keys=True)
        j.write(encoded_state)


def RecoverState(args=[DEFAULT_PATH]):
    """Recovers the state of diary from JSON args[0]:=path"""
    global state
    if len(args) != 1:
        raise ArgumentError("Too many parameters")
    path = args[0]
    try:
        with open(path, "r", encoding="UTF-8") as j:
            state = jsonpickle.decode(j.read(), keys=True)
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
        command, args = None, []
        try:
            command, *args = input().split()
        except ValueError:
            continue
        if command == "help":
            for c in commands.items():
                print(f"{c[0]} args:  <{'> <'.join(c[1].args)}> {c[1].description}")

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


DEFAULT_PATH = 'r.json'
# RecoverState(DEFAULT_PATH)

mainLoop(DEFAULT_PATH, comms)
C = Area(name="ar", type=3, days={
    datetime.date.today(): Day(date=datetime.date.today(), items={"it": Item(name="it", data="what", meta={})})},
         item_templates={"te": ItemTemplate("te", {"question": "nani", "enabled": True})})
state[C.name] = C
SaveState((DEFAULT_PATH,))
RecoverState((DEFAULT_PATH,))
