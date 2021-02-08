from dataclasses import dataclass
import datetime


# Area > Day > Item
class AreaTypes:
    CHECKLIST = 1
    STRUCTURED_DATA = 2
    FREE_TEXT = 3


@dataclass
class Area:
    name: str
    type: int
    days: dict
    item_templates: dict


@dataclass
class Day:
    date: datetime
    items: dict  # for FREETEXT: items has one element


@dataclass
class Item:
    name: str
    data: str  # for CHECKLIST bool
    #meta: dict


@dataclass
class ItemTemplate:
    name: str
    meta: dict  # enabled, question


class Command:
    def __init__(self, name, description, function, args=[]):
        self.name = name
        self.description = description
        self.function = function
        self.args = args


class ArgumentError(ValueError):
    # types: nf(not found), no(number of args),date
    def __init__(self, etype, lower=None, upper=None):
        e = ""
        if etype == "nf":
            e = f"Error: Such {lower} not found"
        elif etype == "no":
            if upper is not None:
                e = f"Error: expected number of arguments between {lower} and {upper}."
            else:
                e = f"Error: expected number of arguments: {lower}"
        elif etype == "date":
            e = "Error: Wrong date format. Expected YYYY-MM-DD"
        else:
            e = etype
        self.strerror = e
        self.args = {e}
