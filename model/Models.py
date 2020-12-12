
# Area > Day > Item
class Area():
    def __init__(self,name,days,type):
        self.name = name
        self.days = days
        self.type = type #checklist,sematicData,freetext


class Day():
    def __init__(self,items,date):
        self.date = date
        self.items = items


class Item():
    def __init__(self,data,meta):
        self.data = data
        self.meta = meta

class Command:
    def __init__(self,name,description,function,args=[]):
        self.name = name
        self.args = args
        self.description= description
        self.function = function
