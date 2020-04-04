#This is a deprecated and downright shitty codebase. There are a billion seperate requests that should be refactored.
#It was done quick and dirty to get things off the ground and  working. My work partners repo should house 
#the updated codebase that removes a ton of crap. If, for some reason, you are relying
#on this code, I am sorry and may  god have mercy on your soul.
import requests
import config
# import xlsxwriter
import pygsheets
import pandas as pd

#google auth stuff
api = pygsheets.authorize()
#gsheet
wb = api.open('TEST')
sheet = wb.worksheet_by_title('Sheet2')

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
API_KEY = config.CENSUS_API_KEY
URL = 'https://api.census.gov/data/'
YEAR = '2018/'
DATA_SET = 'acs/acs5'
BASE_URL = URL + YEAR + DATA_SET
GET = '?get='
MED_GROSS_RENT = 'B25064_001E'
MED_GROSS_RENT_DOLLARS = 'B25064_001E'
GROSS_RENT_TOTAL = 'B25063_001E'
GROSS_RENT_PERCENT_INCOME_30_34 = 'B25070_007E'
GROSS_RENT_PERCENT_INCOME_35_39 = 'B25070_008E'
GROSS_RENT_PERCENT_INCOME_40_49 = 'B25070_009E'
GROSS_RENT_PERCENT_INCOME_50_PLUS = 'B25070_010E'
TOTAL_POPULATION_BURDENED = 'B25070_001E'


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
# this string will get the population of individuals that pay 50% or more of their income
# in rent for all counties in oregon.
# It returns a list of lists. The first list containing meta data and the following lists containing the requested info.
# i.e. one list being ['5690', '41', '047'], meaning 5690 people spend 50% or more of their income on rent in the county 047 (FIPS code for Marion county) in the state 41 (FIPS code for Oregon)
FINAL_URL = BASE_URL \
    + GET + GROSS_RENT_PERCENT_INCOME_50_PLUS + COMMA\
    + GROSS_RENT_PERCENT_INCOME_30_34 + COMMA\
    + GROSS_RENT_PERCENT_INCOME_35_39 + COMMA\
    + GROSS_RENT_PERCENT_INCOME_40_49 + COMMA\
    + TOTAL_POPULATION_BURDENED\
    + FOR + COUNTY + "*" \
    + IN + STATE + OREGON

r = requests.get(url=FINAL_URL + API_KEY)
# values is the return value from the census  API
values = r.json()
print(values)
# household_incomes = {}
# NUM_HOUSEHOLD_INCOME_VARIABLES = 17
# for i in range(2, NUM_HOUSEHOLD_INCOME_VARIABLES + 1):
#     # B19001_00 + i + E is a range of income variables in the acs5
#     FINAL_URL = BASE_URL \
#         + GET + ('B19001_00' if i < 10 else 'B19001_0') + str(i) + 'E' \
#         + FOR + COUNTY + "*" \
#         + IN + STATE + OREGON
#     r = requests.get(url=FINAL_URL + API_KEY)
#     values = r.json()
#     # get number of individuals in ith bracket and match with respective key
#     for i in range(1, len(values)):
#         # add to household_income the value which matches the fips value which matches the key in fips_codes
#         # household_incomes[fips_codes[values[i][2]]].append(int(values[i][0]))
#         # fips_codes[047] = Marion
#         # int(values[1][0]) = 5690
#         # household_incomes[Marion].append(int(5690)
#         # household_incom = {Marion: [5690]}
#         household_incomes[fips_codes[values[i][2]]].append(int(values[i][0]))


# trends = {}
# for i in range(2011,2019):
#     FINAL_URL =  URL + str(i) + '/' + DATA_SET\
#     + GET + TOTAL_POPULATION_BURDENED + COMMA + GROSS_RENT_PERCENT_INCOME_50_PLUS + COMMA\
#     + GROSS_RENT_PERCENT_INCOME_30_34 + COMMA + GROSS_RENT_PERCENT_INCOME_35_39 + COMMA + GROSS_RENT_PERCENT_INCOME_40_49\
#     + COMMA + MED_GROSS_RENT_DOLLARS\
#     + FOR + COUNTY + "*" \
#     + IN + STATE + OREGON

#     r = requests.get(url=FINAL_URL + API_KEY)
#     values = r.json()
#     for i in range(1, len(values)):
#         trends[fips_codes[values[i][7]]].append(100 * (int(values[i][1])/int(values[i][0])))
#         trends[fips_codes[values[i][7]]].append(100 * ((int(values[i][2])) + (int(values[i][3])) + (int(values[i][4])))/int(values[i][0]))
#         trends[fips_codes[values[i][7]]].append(int(values[i][5]))


# df_route = pd.read_csv('https://openmv.net/file/travel-times.csv')
# sheet.set_dataframe(df_route, (1,1))