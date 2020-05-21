import unittest
import unittest.mock
from unittest.mock import Mock
import unittest.mock as mock
from google import Google
import pygsheets
from pygsheets import authorize
from pygsheets import client


class TestGSheet(unittest.TestCase):

    @mock.patch('google.pygsheets.authorize') #mock the authorize call from pygsheets inside our Google class
    def test_authorizes(self, mock_authorize):
        """
        Test that pygsheets returns a client on authorization
        """
        mock_authorize.return_value = client
        response = Google.auth(self, 'FAKE')
        self.assertEqual(response, mock_authorize.return_value)

    @mock.patch('google.pygsheets.authorize.open')
    def test_opens_worksheet(self, mock_open):
        1  == 1


if __name__ == '__main__':
    unittest.main()