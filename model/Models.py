from dataclasses import dataclass
import datetime


# Area > Day > Item
class AreaTypes:
    CHECKLIST = 1
    SEMANTIC_DATA = 2
    FREE_TEXT = 3


@dataclass
class Area:
    name: str
    type: int
    days: dict
    item_templates: dict


@dataclass
class Item:
    name: str
    data: str
    meta: dict  # enabled, question


@dataclass
class ItemTemplate:
    name: str
    meta: dict


@dataclass
class Day:
    date: datetime
    items: dict  # freetext: items[]


class Command:
    def __init__(self, name, description, function, args=[]):
        self.name = name
        self.description = description
        self.function = function
        self.args = args


class ArgumentError(ValueError):
    def __init__(self, arg):
        self.strerror = arg
        self.args = {arg}
