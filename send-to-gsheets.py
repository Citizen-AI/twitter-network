# This Python file uses the following encoding: utf-8

from dotenv import load_dotenv
load_dotenv(dotenv_path='./.env', verbose=True)

from distutils.util import strtobool
import os
# import unicodecsv as csv
from oauth2client.service_account import ServiceAccountCredentials
import pandas
import gspread
from gspread_dataframe import set_with_dataframe


print 'Connecting to Google Sheet…'
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(os.getenv('json_keyfile'), scope)
gc = gspread.authorize(credentials)
sheets = gc.open_by_key('1oRsMw3wipn7LHFQlxtpazPoGCpZvM3I0lScUKXCi388')

if strtobool(raw_input('OK to delete & replace test sheet? ')):
    print "Deleting"
    try: sheets.del_worksheet(sheets.worksheet('test'))
    except: print "Couldn't delete"

    faves = pandas.read_csv('faves.csv')

    print "Creating new worksheet"
    new_worksheet = sheets.add_worksheet(title="test", rows=faves.shape[0], cols=faves.shape[1])
    print "Uploading data"
    set_with_dataframe(new_worksheet, faves)
