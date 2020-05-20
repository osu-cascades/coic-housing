# # This codebase is a rework of an original I worked on that pulled the data from the census, manually transformed it,
# # and stored it in excel. This new code gets user input for census acs years, pulls the data,
# # transforms with pandas, and saves to GSheets. With Tableau public (not desktop!),
# # you can have your data automatically sync (every 24 hours it updates but can be done manually if needed sooner).
# # The goal here was to make things as hands off for the client as they aren't very technically proficient.
# # For questions, comments, concerns email taymal1987@gmail.com
import requests
import config
import pygsheets
import pandas as pd
import os
import datetime
import json
from dotenv import load_dotenv
from flask import Flask, abort, request, redirect
load_dotenv()

def pword_validate(pword):
    if(os.environ['FLASK_ENV'] == 'dev'):
        if str(pword) != str(os.getenv('TESTING_PWORD')):
            return '403'
        return '200'
    if str(pword) != str(os.getenv('PWORD')):
        return abort(403)
    return '200'

def year_validate(year):
    now = datetime.datetime.now()
    #oldest acceptable acs year is 2011, but validating with 2013 to maintain trends viz
    if(os.environ['FLASK_ENV'] == 'dev'):
        if int(year) > now.year - 1 or int(year) < 2013:
            return '422'
        return '200'
    if int(year) > now.year - 1 or int(year) < 2013:
        return abort(422)
    return '200'

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return redirect('./index.html')

@app.route('/update_gsheet', methods=['GET'])
def update_sheet():
    data = request.args

    pword_validate(str(data['pword']))
    acs_year = str(data['year'])
    year_validate(acs_year)

    # google auth stuff
    # this does not use os.environ['xxxx']
    # bc pygsheets loads the file with json.loads(os.environ['xxxx'])
    # so only the name of the heroku env var needs to be passed
    if(os.environ['FLASK_ENV'] == 'dev'):
        api = pygsheets.authorize(service_file = os.getenv('SERVICE_ACCOUNT'))
    else:
        api = pygsheets.authorize(service_account_env_var = 'SERVICE_ACCOUNT')
    wb = api.open('COIC-dashboard')

    fips_codes = {
        "001": "Baker",
        "003": "Benton",
        "005": "Clackamas",
        "007": "Clatsop",
        "009": "Columbia",
        "011": "Coos",
        "013": "Crook",
        "015": "Curry",
        "017": "Deschutes",
        "019": "Douglas",
        "021": "Gilliam",
        "023": "Grant",
        "025": "Harney",
        "027": "Hood River",
        "029": "Jackson",
        "031": "Jefferson",
        "033": "Josephine",
        "035": "Klamath",
        "037": "Lake",
        "039": "Lane",
        "041": "Lincoln",
        "043": "Linn",
        "045": "Malheur",
        "047": "Marion",
        "049": "Morrow",
        "051": "Multnomah",
        "053": "Polk",
        "055": "Sherman",
        "057": "Tillamook",
        "059": "Umatilla",
        "061": "Union",
        "063": "Wallowa",
        "065": "Wasco",
        "067": "Washington",
        "069": "Wheeler",
        "071": "Yamhill"
    }
    # API setup and variables
    if(os.environ['FLASK_ENV'] == 'dev'):
        API_KEY = os.getenv('CENSUS_API_KEY')
    else:
        API_KEY = os.environ['CENSUS_API_KEY']
    URL = 'https://api.census.gov/data/'
    YEAR = acs_year + '/'
    DATA_SET = 'acs/acs5'
    BASE_URL = URL + YEAR + DATA_SET
    GET = '?get='
    MED_GROSS_RENT = 'B25064_001E'
    MED_GROSS_RENT_DOLLARS = 'B25064_001E'
    GROSS_RENT_TOTAL = 'B25063_001E'
    GROSS_RENT_PERCENT_INCOME_25_30 = 'B25070_006E'
    GROSS_RENT_PERCENT_INCOME_30_34 = 'B25070_007E'
    GROSS_RENT_PERCENT_INCOME_35_39 = 'B25070_008E'
    GROSS_RENT_PERCENT_INCOME_40_49 = 'B25070_009E'
    GROSS_RENT_PERCENT_INCOME_50_PLUS = 'B25070_010E'
    TOTAL_POPULATION_BURDENED = 'B25070_001E'
    MED_INCOME = 'B06011_001E'


    COMMA = ','
    FOR = '&for='
    IN = '&in='
    PLUS = '+'
    STATE = 'state:'
    ALL_STATES = 'state:*'
    COUNTY = 'county:'
    OREGON = '41'
    DESCHUTES = '017'
    CROOK = '013'
    JEFFERSON = '031'

    # FINAL_URL = https://api.census.gov/data/2018/acs/acs5?get=B25070_010E&for=county:*&in=state:41
    # this string will get the population of individuals that pay 30 - 50% of their income
    # in rent for all counties in oregon.
    # i.e. one list being ['5690', '41', '047'], meaning 5690 people sampled spend 50% or more of
    # their income on rent in the county 047 (FIPS code for Marion county) in the state 41 (FIPS code for Oregon)
    FINAL_URL = BASE_URL \
        + GET + GROSS_RENT_PERCENT_INCOME_50_PLUS + COMMA\
        + GROSS_RENT_PERCENT_INCOME_25_30 + COMMA\
        + GROSS_RENT_PERCENT_INCOME_30_34 + COMMA\
        + GROSS_RENT_PERCENT_INCOME_35_39 + COMMA\
        + GROSS_RENT_PERCENT_INCOME_40_49 + COMMA\
        + TOTAL_POPULATION_BURDENED\
        + FOR + COUNTY + '*'\
        + IN + STATE + OREGON

    r = requests.get(url=FINAL_URL + API_KEY)
    # values is the return value from the census  API
    values = r.json()
    df = pd.DataFrame(values)
    df.columns = ['GROSS_RENT_PERCENT_INCOME_50_PLUS', 'GROSS_RENT_PERCENT_INCOME_25_30', 'GROSS_RENT_PERCENT_INCOME_30_34',
                  'GROSS_RENT_PERCENT_INCOME_35_39', 'GROSS_RENT_PERCENT_INCOME_40_49', 'TOTAL_POPULATION_BURDENED', 'state', 'county']
    # pandas return copies so you must place it in a variable
    df = df.drop([0])

    # TODO overall description
    trans_df = pd.DataFrame(df['TOTAL_POPULATION_BURDENED'])
    trans_df['PERCENT RENT BURDENED'] = (pd.to_numeric(df['GROSS_RENT_PERCENT_INCOME_25_30']) + pd.to_numeric(df['GROSS_RENT_PERCENT_INCOME_30_34']) + pd.to_numeric(
        df['GROSS_RENT_PERCENT_INCOME_35_39']) + pd.to_numeric(df['GROSS_RENT_PERCENT_INCOME_40_49'])) / pd.to_numeric(df['TOTAL_POPULATION_BURDENED'])
    trans_df['PERCENT SEVERLY RENT BURDENED'] = pd.to_numeric(
        df['GROSS_RENT_PERCENT_INCOME_50_PLUS']) / pd.to_numeric(df['TOTAL_POPULATION_BURDENED'])
    # get percents from floats
    trans_df['PERCENT SEVERLY RENT BURDENED'] = trans_df['PERCENT SEVERLY RENT BURDENED'] * 100
    trans_df['PERCENT RENT BURDENED'] = trans_df['PERCENT RENT BURDENED'] * 100

    trans_df['COUNTY FIPS'] = df['county']
    trans_df['COUNTY NAME'] = df['county'].map(fips_codes)
    # #gsheet
    wb = api.open('COIC-dashboard')
    sheet = wb.worksheet_by_title('viz burden data')
    sheet.clear()
    sheet.set_dataframe(trans_df, (1, 1))


    county_dict = {
        "013": "Crook",
        "017": "Deschutes",
        "031": "Jefferson"
    }
    # household_income is a dict of lists to store all income brackets ($10,000 to $14,999, $15,000 to $19,999,...$200,000+)
    household_incomes = {}
    for values in county_dict.values():
        household_incomes[values] = []

    NUM_HOUSEHOLD_INCOME_VARIABLES = 17
    for i in range(2, NUM_HOUSEHOLD_INCOME_VARIABLES + 1):
        # B19001_00 + i + E is a range of income variables in the acs5
        FINAL_URL = BASE_URL \
            + GET + ('B19001_00' if i < 10 else 'B19001_0') + str(i) + 'E' \
            + FOR + COUNTY + CROOK + COMMA\
            + DESCHUTES + COMMA \
            + JEFFERSON\
            + IN + STATE + OREGON

        r = requests.get(url=FINAL_URL + API_KEY)
        values = r.json()
        # get number of individuals in ith bracket and match with respective key
        for i in range(1, len(values)):
            # add to household_income the value which matches the fips value which matches the key in fips_codes
            # household_incomes[fips_codes[values[i][2]]].append(int(values[i][0]))
            # fips_codes[047] = Marion
            # int(values[1][0]) = 5690
            # household_incomes[Marion].append(int(5690)
            # household_incom = {Marion: [5690]}
            household_incomes[fips_codes[values[i][2]]].append(int(values[i][0]))

    # TODO overall description
    df = pd.DataFrame.from_dict(household_incomes)
    trans_df = df.transpose()
    trans_df.columns = ['Less than $10,000',	'$10,000 to $14,999',	'$15,000 to $19,999',
                        '$20,000 to $24,999',	'$25,000 to $29,999',	'$30,000 to $34,999',	'$35,000 to $39,999',
                        '$40,000 to $44,999',	'$45,000 to $49,999',	'$50,000 to $59,999',	'$60,000 to $74,999',
                        '$75,000 to $99,999',	'$100,000 to $124,999',	'$125,000 to $149,999',	'$150,000 to $199,999',	'$200,000 or more']
    counties_df = pd.DataFrame.from_dict(county_dict, orient='index')
    counties_df.columns = ['county']
    normalized_df = trans_df.apply(lambda x: x/x.max(), axis=1)

    # pretty print normalized data just for sanity
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(normalized_df)

    # gsheet
    wb = api.open('COIC-dashboard')
    sheet = wb.worksheet_by_title('viz household income data')
    sheet.clear()
    sheet.set_dataframe(counties_df, (1, 1))
    sheet.set_dataframe(normalized_df, (1, 2))

    # TODO overall description
    trends = {}
    for values in county_dict.values():
        trends[values] = []
    # historic rent burdening data used in linear regression viz
    for i in range(2011, int(acs_year) + 1):
        FINAL_URL = URL + str(i) + '/' + DATA_SET\
            + GET + TOTAL_POPULATION_BURDENED + COMMA\
            + GROSS_RENT_PERCENT_INCOME_50_PLUS + COMMA\
            + GROSS_RENT_PERCENT_INCOME_25_30 + COMMA\
            + GROSS_RENT_PERCENT_INCOME_30_34 + COMMA\
            + GROSS_RENT_PERCENT_INCOME_35_39 + COMMA\
            + GROSS_RENT_PERCENT_INCOME_40_49\
            + COMMA + MED_INCOME\
            + FOR + COUNTY + DESCHUTES + COMMA\
            + JEFFERSON + COMMA + CROOK \
            + IN + STATE + OREGON

        r = requests.get(url=FINAL_URL + API_KEY)
        values = r.json()
        for i in range(1, len(values)):
            trends[fips_codes[values[i][8]]].append(
                100 * (int(values[i][1])/int(values[i][0])))
            trends[fips_codes[values[i][8]]].append(100 * ((int(values[i][2])) + (
                int(values[i][3])) + (int(values[i][4]) + (int(values[i][5]))))/int(values[i][0]))
            trends[fips_codes[values[i][8]]].append(int(values[i][6]))


    # TODO overall description
    df = pd.DataFrame.from_dict(trends)
    trans_df = df.transpose()
    burden = trans_df.iloc[:, ::3]
    burden = burden.stack().reset_index()
    burden.rename(columns={'level_0': 'county', 0: 'rent burdened'}, inplace=True)
    severe_burden = trans_df.iloc[:, 1::3]
    severe_burden = severe_burden.stack().reset_index()
    severe_burden.rename(
        columns={'level_0': 'county', 0: 'severe rent burdened'}, inplace=True)
    med_income = trans_df.iloc[:, 2::3]
    med_income = med_income.stack().reset_index()
    med_income.rename(columns={'level_0': 'county',
                               0: 'median income'}, inplace=True)

    final_df = pd.DataFrame(burden['rent burdened'])
    final_df['severe rent burdened'] = severe_burden['severe rent burdened']
    final_df['median income'] = med_income['median income']
    counties = ['Crook', 'Deschutes', 'Jefferson']
    county = [ele for ele in counties for _ in range(
        len(range(2011, int(acs_year) + 1)))]
    final_df['county'] = county
    years = [i for i in range(2011, int(acs_year) + 1)] * 3
    final_df['year'] = years

    sheet = wb.worksheet_by_title('viz historic rent data')
    sheet.clear()
    sheet.set_dataframe(final_df, (1, 1))

    return 'we gucci'
if __name__ == '__main__':
    app.run()
