# adapted from https://medium.com/@agrimabahl/elegant-python-code-reproduction-of-most-common-words-from-a-story-25f5e28e0f8c

from collections import Counter
import sys
import os
import re

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
