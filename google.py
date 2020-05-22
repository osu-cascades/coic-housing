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
        return api.open(book_name)

    def worksheet_by_title_wrapper(self, wb, sheet_title):
        return wb.worksheet_by_title(sheet_title)

    def clear_wrapper(self, sheet):
        sheet.clear()

    def set_dataframe_wrapper(self, sheet, df, tup):
        sheet.set_dataframe(df, tup)