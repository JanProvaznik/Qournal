import jsonpickle
import json
import sys
from Models import *

DEFAULT_PATH = 'q.json'
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
        raise ArgumentError("no", 2)
    name = args[0]
    if name in state:
        raise ArgumentError(f"There is already area with name {name}.")
    area_type_str = args[1]
    area_type = 0
    if area_type_str in ['1', 'checklist', 'cl']:
        area_type = AreaTypes.CHECKLIST
    elif area_type_str in ['2', 'structuredData', 'structureddata', 'structured_data', 'sd']:
        area_type = AreaTypes.STRUCTURED_DATA
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
    if len(args) != 1:
        raise ArgumentError("no", 1)
    name = args[0]
    if name in state:
        decision = input(f"Do you really want to delete the {name} area? Y/n 1/0")
        if decision in ["1", "Y", "y", "yes"]:
            del state[name]
            return True
        return False
    else:
        raise ArgumentError("nf", "Name of area")


def ChangeArea(args):
    """ Used for redefining the area's items
     args[0] := name"""
    global state

    # error handling
    if len(args) != 1:
        raise ArgumentError("no", 1)
    area_name = args[0]
    if area_name not in state:
        raise ArgumentError("nf", "area")

    area = state[area_name]

    def ChangeItemTemplate(template):
        new_name = input(f"Enter new name for {template.name} (or press enter)")
        new_question = input("Enter new question (or press enter to keep)")
        is_enabled = input("Enable this area? Y/N") in {'y', 'Y', '1', 'yes', 'Yes', ""}
        # change question if entered
        if len(new_question) == 0:
            new_question = template.meta["question"]
        # rename
        if len(new_name) > 0:
            old_name = template.name
            old_template = area.item_templates.pop(old_name)
            old_template.name = new_name
            area.item_templates[new_name] = old_template

            # rename all items inside days in this area
            for day in area.days.values():
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
    if area.type == AreaTypes.CHECKLIST or area.type == AreaTypes.STRUCTURED_DATA:
        print(f"There currently these item templates: {' '.join(templates)}")
        while True:
            try:
                comm, *item_args = input("Enter command: addi to add an item template,"
                                         " chai <name> to change an item template,"
                                         " exit to exit the change area subprogram.").split()
            except ValueError:  # no command given
                continue
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
    # possible upgrade: only selected date range
    global state
    # error handling
    if len(args) != 1:
        raise ArgumentError("no", "1")
    area_name = args[0]
    if area_name not in state:
        raise ArgumentError("nf", "area")

    area = state[area_name]
    print(area.name)

    length_of_date_and_spacing = 12
    # table with colsize same as name of item
    if area.type == AreaTypes.CHECKLIST:
        displayed_item_names = []
        print(" " * length_of_date_and_spacing, end="")
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
                    # converts value to  checklist character + spacing
                    if day.items[name].data in {"N", "n", "no", "x", "X", "0", "false", "F", "f", ""}:
                        print("x", end=" " * (len(name)))
                    else:
                        print("v", end=" " * (len(name)))

                else:
                    # this item is not present in this day, just put spaces there
                    print(" " * (len(name) + 1), end='')
            print()
        print()

    # table with colsize equal to max of answers or names
    elif area.type == AreaTypes.STRUCTURED_DATA:
        displayed_item_names_with_lengths = {}
        print(" " * length_of_date_and_spacing, end="")
        # table head initialization
        for item_template in area.item_templates.values():
            if item_template.meta['enabled']:
                displayed_item_names_with_lengths[item_template.name] = len(item_template.name)
        # table values initialization
        for day in sorted(area.days.values(), key=lambda x: x.date):
            for name in displayed_item_names_with_lengths.keys():
                if name in day.items:
                    displayed_item_names_with_lengths[name] = max(
                        len(day.items[name].data), displayed_item_names_with_lengths[name])
        # print table head
        for item_name, length in displayed_item_names_with_lengths.items():
            print(item_name, end=' ')
            print(" " * (length - len(item_name)), end='')
        print()
        # print table content
        for day in sorted(area.days.values(), key=lambda x: x.date):
            print(day.date.isoformat(), end=': ')
            for name, length in displayed_item_names_with_lengths.items():
                if name in day.items:
                    printed_value = day.items[name].data
                    print(printed_value, end='')
                    print(" " * (length - len(printed_value) + 1), end='')
                else:
                    print(" " * (length + 1), end='')
            print()
        print()

        pass
    # simple print, one day on one line
    elif area.type == AreaTypes.FREE_TEXT:
        for day in sorted(area.days.values(), key=lambda x: x.date):
            print(f"{day.date}: {list(day.items.values())[0].data}")
        print()
    else:
        return False
    return True


def ParseAddDay(args=None):
    """Helper function for determining the correct day from input."""
    if args is None:
        args = []
    if len(args) > 1:
        raise ArgumentError("no", 0, 1)

    which_day = None
    if not args:
        which_day = datetime.date.today()
    elif type(args[0]) is datetime.date:
        which_day = args[0]
    elif type(args[0]) is str:
        if args[0] in ["y", "yesterday"]:
            which_day = datetime.date.today() - datetime.timedelta(days=1)
        else:
            try:
                which_day = datetime.date.fromisoformat(args[0])
            except ValueError:
                raise ArgumentError("date")
    else:
        raise ArgumentError("date")
    return which_day


def AddDayToArea(args):
    """Adds day to specified area.
    first arg, which day, second which area
    """
    global state
    area = state[args[1]]
    day = Day(args[0], {})
    for template in area.item_templates.values():
        if template.meta['enabled']:
            answer = input(template.meta['question'] + " ")
            if args[0] in area.days and answer == "": # keep old entry if new is empty
                answer = area.days[args[0]].items[template.name].data
            item = Item(template.name, answer)
            day.items[template.name] = item
    area.days[args[0]] = day


def AddDayToOneArea(args):
    """Prompts questions and adds day to specific area, args[0] name of area,
    args[1] date in iso format or 'y' for yesterday, can be left blank for today """
    if len(args) < 1 or len(args) > 2:
        raise ArgumentError("no", 1, 2)
    area, which_day = None, None
    if args[0] in state:
        area = state[args[0]]
    else:
        raise ArgumentError("nf", "area")
    if len(args) == 2:
        which_day = ParseAddDay([args[1]])
    else:
        which_day = ParseAddDay()
    AddDayToArea([which_day, area.name])
    return True


def AddDayToAllAreas(args):
    """Prompts all questions and adds day to all areas
    args[0]:= date in iso format or 'y' for yesterday, can be left blank for today"""
    which_day = ParseAddDay(args)
    for area in state.values():
        AddDayToArea([which_day, area.name])
    return True


def SaveState(args):
    """Puts the state of diary to JSON
    args[0]:= path to JSON (optional)"""
    global state
    if len(args) > 1:
        raise ArgumentError("no", 0, 1)
    if not args:
        args = [DEFAULT_PATH]
    with open(args[0], "w+", encoding="UTF-8") as j:
        encoded_state = jsonpickle.encode(state, keys=True)
        j.write(encoded_state)
        return True


def RecoverState(args):
    """Recovers the state of diary from JSON
    args[0]:=path to JSON (optional)"""
    global state
    if len(args) > 1:
        raise ArgumentError("no", 0, 1)
    if not args:
        args = [DEFAULT_PATH]
    path = args[0]
    try:
        with open(path, "r", encoding="UTF-8") as j:
            try:
                state = jsonpickle.decode(j.read(), keys=True)
            except json.decoder.JSONDecodeError:
                state = {}

            return True
    except FileNotFoundError:
        print("Warning: Invalid path to JSON. Creating new one.")
        f = open(path, "w+")
        f.close()
        state = {}
        return True


def Exit(args):
    if not args:
        print("Bye")
        SaveState([DEFAULT_PATH])
        sys.exit()
    elif args[0] in {"no", "0", "nosave"}:
        print("Bye")
        sys.exit()
    else:
        return False


def MainLoop(commands):
    """Loop that parses and runs commands."""
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
                print(f"{c[0]} | args:  <{'> <'.join(c[1].args)}> |  {c[1].description}")
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


# commands definitions
comms = {
    "listas": Command("listarea", "lists available areas", ListAreas),
    "adda": Command("addarea", "adds area and runs the change area subprogram types: 1-checklist, 2-structured data, "
                               "3-free text", AddArea, ["name", "type"]),
    "rema": Command("removearea", "removes specified area", RemoveArea, ["name"]),
    "changea": Command("changearea", "runs the change area subprogram", ChangeArea, ["name"]),
    "dispa": Command("displayarea", "displays specified area", DisplayArea, ["name"]),
    "addall": Command("adddaytoall", "runs the add day subprogram for all areas", AddDayToAllAreas, ["date?"]),
    "addspec": Command("adddaytospecific", "runs the add day subprogram for specified area, date blank for today, "
                                           "in iso format or 'y' for yesterday", AddDayToOneArea, ["name", "date?"]),
    "commit": Command("commit", "commits data to json", SaveState, ["path?"]),
    "recover": Command("recover", "recovers data from json", RecoverState, ["path?"]),
    "exit": Command("exit", "exits", Exit, ["nosave?"])
    # possible extension: plots from structuredData and checklists
}

RecoverState([DEFAULT_PATH])
MainLoop(comms)
SaveState([DEFAULT_PATH])
