from app import *
import pytest
from dotenv import load_dotenv
import os

@pytest.fixture
def incorrect_pword():
    pword = 'wrong password'
    return pword

def test_wrong_passwords_are_not_accepted(incorrect_pword):
    assert pword_validate(incorrect_pword) == '403'

def test_correct_passwords_are_accepted():
    pword = 'test'
    assert pword_validate(pword) == '200'

def test_year_must_be_greater_than_2011():
    year = 2013
    assert year_validate(year) == '200'

def test_year_cant_be_less_than_2010():
    year = 2010
    assert year_validate(year) == '422'