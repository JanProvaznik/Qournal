from unittest.mock import patch
import unittest

from main import *

class Tests(unittest):
    def __init__(self):
        pass
    def test_changeArea(self):
        pass
C = Area(name="ar", type=3, days={
    datetime.date.today(): Day(date=datetime.date.today(), items={"it": Item(name="it", data="what", meta={})})},
         item_templates={"te": ItemTemplate("te", {"question": "nani", "enabled": True})})
state[C.name] = C
SaveState((DEFAULT_PATH,))
RecoverState((DEFAULT_PATH,))
