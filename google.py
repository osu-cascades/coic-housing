import os
import pygsheets

class Google(object):
    def __init__(self):
        super().__init__()

    def auth(self, creds):
        if(os.environ['FLASK_ENV'] == 'dev'):
            api = pygsheets.authorize(service_file = os.getenv(creds))
        else:
            api = pygsheets.authorize(service_account_env_var = creds)
        return api

    def open_workbook(self, api, book_name):
        api.open(book_name)