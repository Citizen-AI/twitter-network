# adapted from https://medium.com/@agrimabahl/elegant-python-code-reproduction-of-most-common-words-from-a-story-25f5e28e0f8c

from collections import Counter
import sys
import os
import re
import connect_to_google_sheets
import pandas as pd
from gspread_dataframe import set_with_dataframe
from distutils.util import strtobool


OUTPUT_FOLDER = 'output/'


def wordcount(text, n):
    stopwords = set(line.strip() for line in open('stopwords.txt'))
    stopwords = stopwords.union(set(['a', 'i', 'amp', 'youre', 'ive', 'im', 'yep']))
    wordcount = Counter()

    pattern = r"\W"
    for word in text.lower().split():
        word = re.sub(pattern, '', word)
        if word not in stopwords:
            wordcount[word] += 1

    return wordcount.most_common(n)


def print_err(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(e, exc_type, fname, exc_tb.tb_lineno)
    # TODO: errors in red


def column_contains_value(data_frame, column, value):
    return len(data_frame[data_frame[column].str.match(value)]) is not 0


def csv_to_gsheet(csv_file_names, google_sheet_key):
    sheets = connect_to_google_sheets.sheets(google_sheet_key)
    if type(csv_file_names) is not list: csv_file_names = [csv_file_names]
    for csv_file_name in csv_file_names:
        df = pd.read_csv(csv_file_name)
        confirm = input('OK to delete & replace worksheets? (Y/n) ')
        if confirm is '' or strtobool(confirm):
            print('Deleting')
            try: sheets.del_worksheet(sheets.worksheet(csv_file_name))  # note we can't have no worksheets
            except Exception as e: print_err(e)
            print('Creating new worksheet')
            worksheet = sheets.add_worksheet(title=csv_file_name, rows=df.shape[0], cols=df.shape[1])
            print('Uploading',csv_file_name)
            set_with_dataframe(worksheet, df)


def pd_to_csv(df, filename):
    print('Writing to', filename)
    df.to_csv(OUTPUT_FOLDER + filename, index=False, encoding='utf8')


def clean(text_list):
    '''Get rid of links, mentions and hashtags'''
    return [re.sub(r'\bhttps?://t.co/.+?\b|@.+?\b|#.+?\b|&amp;', ' ', line) for line in text_list]
