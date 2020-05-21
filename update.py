import os
import datetime
from flask import Flask, abort, request, redirect

class Update(object):
    def __init__(self):
        pass

    def get_census_api_key(self):
        if(os.environ['FLASK_ENV'] == 'dev'):
            return os.getenv('CENSUS_API_KEY')
        else:
            return os.environ['CENSUS_API_KEY']

    def pword_validate(self, pword):
        if str(pword) != str(os.getenv('PWORD')):
            return abort(403)
        return 'passed'

    def year_validate(self, year):
        now = datetime.datetime.now()
        #oldest acceptable acs year is 2011, but validating with 2013 to maintain trends viz
        if(os.environ['FLASK_ENV'] == 'dev'):
            if int(year) > now.year - 1 or int(year) < 2013:
                return abort(422)
            return
        if int(year) > now.year - 1 or int(year) < 2013:
            return abort(422)
        return