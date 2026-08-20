import unittest
import time
from appt_io import parse_appt, parse_agenda, read_agenda
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class TestAppt(unittest.TestCase):
    """Basic Unit Tests for Appt class"""

    def setUp(self):
        self.coffee = parse_appt("2019-01-01 08:00 10:00 | Coffee with neighbors")
        self.coffee_same = parse_appt("2019-01-01 08:00 10:00 | Should be same as coffee")
        self.brunch = parse_appt("2019-01-01 09:00  13:00 | Brunch with neighbors")
        self.brunch_same = parse_appt("2019-01-01 09:00  13:00 | Should be same as brunch")
        self.more_coffee = parse_appt("2019-01-01 13:00 15:00 | More coffee")
        self.naptime = parse_appt("2019-01-01 16:00 18:00 | Afternoon nap")
        self.last_year = parse_appt("2018-01-01 09:00  13:00 | Brunch with neighbors")
        self.next_month = parse_appt("2019-02-01 09:00  13:00 | Brunch with neighbors")

    def test_00_equality(self):
        self.assertTrue(self.brunch == self.brunch)
        self.assertTrue(self.coffee == self.coffee_same)
        self.assertTrue(self.coffee != self.brunch)

    def test_01_order(self):
        self.assertTrue(self.coffee < self.more_coffee)
        self.assertFalse(self.coffee > self.more_coffee)
        self.assertTrue(self.more_coffee > self.coffee)
        self.assertFalse(self.more_coffee < self.coffee)
        self.assertTrue(self.last_year < self.brunch)
        self.assertTrue(self.brunch < self.next_month)
        self.assertTrue(self.naptime > self.more_coffee)

    def test_02_overlap(self):
        self.assertTrue(self.coffee.overlaps(self.brunch))
        self.assertTrue(self.brunch.overlaps(self.coffee))
        self.assertFalse(self.coffee.overlaps(self.more_coffee))
        self.assertFalse(self.brunch.overlaps(self.more_coffee))

    def test_03_intersect(self):
        coffee_at_brunch = self.coffee.intersect(self.brunch)
        self.assertEqual(coffee_at_brunch,
                         parse_appt("2019-01-01 09:00 10:00 | Title doesn't matter"))
        # Original appointments should be unmodified
        self.assertEqual(self.coffee, self.coffee_same)
        self.assertEqual(self.brunch, self.brunch_same)

if __name__ == "__main__":
    unittest.main()
