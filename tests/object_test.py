import json
import sys, os, unittest, configparser, asyncio

import datetime

sys.path.insert(0, os.getcwd())

from sancus.functions.objects import *

class Connections(unittest.TestCase):

    def test_warning_correct(self):
        date = datetime.datetime.utcnow()

        warningData = {
            "username":"Solar",
            "id":4040404,
            "reason":"test",
            "date":date
        }

        warningObj = warningObject(
            username="Solar",
            id= 4040404,
            reason= "test",
            date=date
        )

        self.assertEqual(warningObj.__dict__, warningData, "Warning Object Is Not Working Correctly")

    def test_warning_id_str(self):
        date = datetime.datetime.utcnow()

        warningData = {
            "username":"Solar",
            "id":"a4040404",
            "reason":"test",
            "date":date
        }

        warningObj = warningObject(
            username="Solar",
            id= "a4040404",
            reason= "test",
            date=date
        )

        self.assertEqual(warningObj.__dict__, warningData, "Warning Object Is Not Working Correctly")