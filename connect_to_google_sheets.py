# This Python file uses the following encoding: utf-8

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os

def sheets():

    print('Connecting to Google Sheet…')
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(os.getenv('json_keyfile'), scope)
    gc = gspread.authorize(credentials)
    return gc.open_by_key(os.getenv('google_sheet_key'))
