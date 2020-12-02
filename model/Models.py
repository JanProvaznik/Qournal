
# Area > Day > Item
class Area():
    def __init__(self,name,days,type):
        self.name = name
        self.days = days
        self.type = type #checklist,sematicData,freetext


class Day():
    def __init__(self,items):
        self.items = items


class Item():
    def __init__(self,data,meta):
        self.data = data
        self.meta = meta

