import unittest
from app import app
from update import Update
from werkzeug.exceptions import NotFound, UnprocessableEntity


class TestYear(unittest.TestCase):
    def test_correct_year(self):
        """
        Test that it accepts correct year
        """
        update = Update()
        self.assertIsNone(update.year_validate(2013))

    def test_incorrect_year(self):
        """
        Tests that it aborts (422 status) on year  < 2012
        """
        with self.assertRaises(UnprocessableEntity):
            update = Update()
            update.year_validate(2011)

if __name__ == '__main__':
    unittest.main()