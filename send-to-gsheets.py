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

pivoted = faves.pivot_table(index=['from','to'],aggfunc='count')
pivoted.reset_index(level=['from', 'to'], inplace=True)
pivoted.columns = ['from', 'to', 'count']

confirm = raw_input('OK to delete & replace worksheet? (Y/n) ')
if confirm is '' or strtobool(confirm):
    print "Deleting"
    try: sheets.del_worksheet(sheets.worksheet('faves'))
    except: print "Couldn't delete"

    print "Creating new worksheet"
    new_worksheet = sheets.add_worksheet(title="faves", rows=faves.shape[0], cols=faves.shape[1])
    print "Uploading data"
    set_with_dataframe(new_worksheet, pivoted)
