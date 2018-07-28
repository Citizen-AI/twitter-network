# This Python file uses the following encoding: utf-8

from dotenv import load_dotenv
load_dotenv(dotenv_path='./.env', verbose=True)

from distutils.util import strtobool
import os
from oauth2client.service_account import ServiceAccountCredentials
import pandas
import gspread
from gspread_dataframe import set_with_dataframe


print 'Connecting to Google Sheet…'
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(os.getenv('json_keyfile'), scope)
gc = gspread.authorize(credentials)
sheets = gc.open_by_key(os.getenv('google_sheet_key'))

faves = pandas.read_csv('faves.csv')

faves_pivot = faves.pivot_table(index=['from','to'],aggfunc='count')
faves_pivot.reset_index(level=['from', 'to'], inplace=True)
faves_pivot.columns = ['from', 'to', 'count']

people = pandas.read_csv('people.csv')

confirm = raw_input('OK to delete & replace worksheets? (Y/n) ')
if confirm is '' or strtobool(confirm):
    print "Deleting"
    try: # currently needs one useless worksheet hanging about (can't delete all sheets)
        sheets.del_worksheet(sheets.worksheet('faves'))
        sheets.del_worksheet(sheets.worksheet('people'))
    except: print "Couldn't delete"

    print "Creating new worksheets"
    faves_worksheet = sheets.add_worksheet(title="faves", rows=faves_pivot.shape[0], cols=faves_pivot.shape[1])
    people_worksheet = sheets.add_worksheet(title="people", rows=people.shape[0], cols=people.shape[1])
    print "Uploading faves"
    set_with_dataframe(faves_worksheet, faves_pivot)
    print "Uploading people"
    set_with_dataframe(people_worksheet, people)
