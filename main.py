import jsonpickle
import sys
from model.Models import *

DEFAULT_PATH = 'r.json'
state = {}


def ListAreas(args):
    """Lists defined areas"""
    for a in state.keys():
        print(a)
    return True


def AddArea(args):
    """Creates an area and then runs the change area subprogram.
    args[0]:= name, args[1] := type"""
    if not len(args) == 2:
        raise ArgumentError("Error: 2 arguments required: name and type")
    name = args[0]
    area_type_str = args[1]
    area_type = 0
    if area_type_str in ['1', 'checklist', 'cl']:
        area_type = AreaTypes.CHECKLIST
    elif area_type_str in ['2', 'semanticData', 'semanticdata', 'semantic_data', 'sd']:
        area_type = AreaTypes.SEMANTIC_DATA
    elif area_type_str in ['3', 'freetext', 'ft']:
        area_type = AreaTypes.FREE_TEXT
    else:
        raise ArgumentError("Wrong type of area.")
    new_area = Area(name, area_type, {}, {})
    state[name] = new_area
    print(f"Created area {name} of type {area_type_str}. Executing change area subprogram.")
    ChangeArea([name])
    return True


def RemoveArea(args):
    """Removes selected area, with confirmation.
    args[0]:= name"""
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
    """ Used for redefining the area's items
     args[0] := name"""
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
        is_enabled = input("Enable this area? Y/N") in {'y', 'Y', '1', 'yes', 'Yes', ""}
        # change question if entered
        if len(new_question) == 0: new_question = template.meta["question"]
        # rename
        if len(new_name) > 0:
            old_name = template.name
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
    # subprogram loop for changing an area
    if area.type == AreaTypes.CHECKLIST or area.type == AreaTypes.SEMANTIC_DATA:
        print(f"There currently these item templates: {' '.join(templates)}")
        while True:
            comm, *item_args = input("Enter command: addi to add an item template,"
                                     " chai <name> to change an item template,"
                                     " exit to exit the change area subprogram.").split()
            if comm == "addi" and len(item_args) == 0:
                AddItemTemplate()
            elif comm == "chai" and len(item_args) == 1:
                if item_args[0] in area.item_templates.keys():
                    ChangeItemTemplate(templates[item_args[0]])
                else:
                    print("No such item.")
            elif comm == "exit":
                return True
            else:
                print("No such command. Try again.")

    # freetext has only one item
    elif area.type == AreaTypes.FREE_TEXT:
        if not templates:
            AddItemTemplate()
        else:
            ChangeItemTemplate(list(templates.values())[0])
    else:
        raise ValueError


def DisplayArea(args):
    """Displays area depending on its type.
     args[0]:=name of area"""
    # todo:possible upgrade: only selected date range
    global state
    # error handling
    if len(args) != 1:
        raise ArgumentError("Wrong number of parameters. Expected 1.")
    area_name = args[0]
    if area_name not in state:
        raise ArgumentError(f"No area of name {area_name}")
    area = state[area_name]
    print(area.name)

    # table with colsize same as name of item
    if area.type == AreaTypes.CHECKLIST:
        # used for correct spacing
        displayed_item_names = []
        print(" " * 10 + "  ", end="")
        # table head
        for item_template in area.item_templates.values():
            if item_template.meta['enabled']:
                print(item_template.name, end=" ")
                displayed_item_names.append(item_template.name)
        print()
        # table values
        for day in sorted(area.days.values(), key=lambda x: x.date):
            print(day.date, end=": ")
            for name in displayed_item_names:
                if name in day.items:
                    # converts value to bool (it's checklist), spacing
                    print(bool(day.items[name]), end=" " * (len(name) - 3))
                else:
                    # this item is not present in this day, just put spaces there
                    print(" " * (len(name) + 1))
            print()
        print()

    # table with colsize equal to max of answers or 30.
    elif area.type == AreaTypes.SEMANTIC_DATA:
        # todo pretty print
        """
        displayed_item_names = []
        print(" " * 10 + "  ", end="")
        # table head
        for item_template in area.item_templates.values():
            if item_template.meta['enabled']:
                print(item_template.name, end=" ")
                displayed_item_names.append(item_template.name)
        print()
        # table values
        for day in sorted(area.days.values(), key=lambda x: x.date):
            print(day.date, end=": ")
            for name in displayed_item_names:
                if name in day.items:
                    # converts value to bool (it's checklist), spacing
                    print(bool(day.items[name]), end=" " * (len(name) - 3))
                else:
                    # this item is not present in this day, just put spaces there
                    print(" " * len(name))
            print()
        print()
        """
        pass
    # simple print, one day on one line
    elif area.type == AreaTypes.FREE_TEXT:
        for day in sorted(area.days.values(), key=lambda x: x.date):
            print(f"{day.date}: {list(day.items.values())[0].data}")
            print()
    return True


def AddDay(args):
    """Prompts all questions and adds day to all areas
    args[0]:= date in iso format or 'y' for yesterday, can be left blank for today"""
    if len(args) > 1:
        raise ArgumentError("Wrong number of arguments, expected 0 or 1.")
    if not args:
        args = [datetime.date.today()]
    which_day = None

    if type(args[0]) is datetime.date:
        which_day = args[0]
    elif type(args[0]) is str:
        if args[0] in ["y", "yesterday"]:
            which_day = datetime.date.today() - datetime.timedelta(days=1)
        else:
            try:
                which_day = datetime.date.fromisoformat(args[0])
            except ValueError:
                raise ArgumentError("Wrong date format. Expected YYYY-MM-DD")
    else:
        raise ArgumentError("Wrong date format. Expected YYYY-MM-DD")
    for area in state.values():
        AddDayToArea([which_day, area.name])
    return True


def AddDayToArea(args):
    """Adds day to specified area.
    first arg, which day, secodnd which area
    """
    global state
    area = state[args[1]]
    day = Day(args[0], {})
    for template in area.item_templates.values():
        if template.meta['enabled']:  # todo checklist
            answer = input(template.meta['question'])
            item = Item(template.name, answer, {})
            day.items[template.name] = item
    area.days[args[0]] = day


def SaveState(args):
    """Puts the state of diary to JSON"""
    global state
    if len(args) > 1:
        raise ArgumentError("Too many arguments.")
    if not args:
        args = [DEFAULT_PATH]
    with open(args[0], "w+", encoding="UTF-8") as j:
        encoded_state = jsonpickle.encode(state, keys=True)
        j.write(encoded_state)
        return True


def RecoverState(args):
    """Recovers the state of diary from JSON
    args[0]:=path"""
    global state
    if len(args) > 1:
        raise ArgumentError("Too many parameters")
    if not args:
        args = [DEFAULT_PATH]
    path = args[0]
    try:
        with open(path, "r", encoding="UTF-8") as j:
            state = jsonpickle.decode(j.read(), keys=True)
            return True
    except FileNotFoundError:
        print("Error: Invalid path to JSON.")
        return False


# basic commands definitions
comms = {
    "listas": Command("listarea", "lists available areas", ListAreas),
    "adda": Command("addarea", "adds area and runs the change area subprogram", AddArea, ["name", "type"]),
    "rema": Command("removearea", "removes specified area", RemoveArea, ["name"]),
    "changea": Command("changearea", "runs the change area subprogram", ChangeArea, ["name"]),
    "dispa": Command("displayarea", "displays specified area", DisplayArea, ["name"]),
    "addall": Command("adddaytoall", "runs the add day subprogram for all areas", AddDay, ["date"]),
    # "addspec": Command("adddaytospecific", "runs the add day subprogram for specified area", AddDay, ["name"]),
    "commit": Command("commit", "commits data to json", SaveState, ["path"]),
    "recover": Command("recover", "recovers data from json", RecoverState, ["path"])
    # todo: extension: plots from sematicdata and checklists
}


def mainLoop(path, commands):
    global state
    print("for the list of commands type 'help'")
    while True:
        command, args = None, []
        try:
            command, *args = input().split()
        except ValueError:
            continue
        if command == "help":
            for c in commands.items():
                print(f"{c[0]} ; args:  <{'> <'.join(c[1].args)}> ; {c[1].description}")

        elif command == "exit":
            print("Bye")
            sys.exit()
        else:
            if command in commands:
                try:
                    result = commands[command].function(args)
                    if not result:
                        print("Action failed.")
                except ArgumentError as e:
                    print(e.strerror)
            else:
                print("no such command")


RecoverState([DEFAULT_PATH])
mainLoop(DEFAULT_PATH, comms)
SaveState([DEFAULT_PATH])
