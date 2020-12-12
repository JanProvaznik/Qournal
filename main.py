#from PySide2.QtWidgets import QApplication, QWidget
#from PySide2.QtCore import Qt
import sys

from model.Models import Area,Command



# app = QApplication(sys.argv)

"""
class DefaultView(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.show()

    def renderAreas(self, event):
        pass
"""

def AddArea(name, data):
    """Creates """
    pass


def RemoveArea(name):
    pass


def ChangeArea(name, values):
    pass


def AddDayToArea(args):
    """Adds day to specified area.
    first arg, which day,
    """
    pass


def SaveState(areas):
    """Puts the state of diary to JSON"""
    outdict = {}
    for a in areas:

        pass


def RecoverState(path):
    """Recovers the state of diary from JSON"""
    return None
    pass


#s = DefaultView()
#app.exec_()
comms = {"listarea":Command("listarea","lists available areas")}
def mainLoop(path,commands):
    print("for the list of commands type 'help'")
    state = RecoverState(path)
    while True:
        command, *args= input().split()
        if command == "help":
            for c in commands:
                print(f"{c.name} {str(*c.args)} {c.description}")
        elif command == "exit":
            print("Bye")
            sys.exit()
        else:
            if command in commands:
                commands[command].function(args,state)
            else:
                print("no such command")

mainLoop("",comms)