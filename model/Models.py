from dataclasses import dataclass
from typing import ClassVar
import datetime
# Area > Day > Item


@dataclass
class Area():
   # CHECKLIST: ClassVar[int] = 1
   # SEMATIC_DATA : ClassVar[int] = 2
   # FREE_TEXT : ClassVar[int] = 3
    name:str
    type:int
    days:dict

    '''def __init__(self, name, type, days=[]):
        self.name = name
        self.type = type  # checklist,semanticData,freetext
        self.days = days'''


@dataclass
class Day:
    date:datetime
    items:dict
    '''    def __init__(self, items, date, time):
        self.date = date
        self.items = items
    '''

@dataclass
class Item():
    data:dict
    meta:dict
    '''
    def __init__(self, data, meta):
        self.data = data
        self.meta = meta  # isDisplayed, question
    '''

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
