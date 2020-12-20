# Area > Day > Item
class Area():
    CHECKLIST = 1
    SEMATIC_DATA = 2
    FREE_TEXT = 3

    def __init__(self, name, days, type):
        self.name = name
        self.days = days
        self.type = type  # checklist,semanticData,freetext


class Day():
    def __init__(self, items, date, time):
        self.date = date
        self.items = items


class Item():
    def __init__(self, data, meta):
        self.data = data
        self.meta = meta  # isDisplayed, question


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
