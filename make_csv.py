# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 08:22:16 2018

@author: Lucien
"""

import dask
import dask.bag as db

import re

from datetime import datetime

dask.config.set(scheduler='threads')

def extract_column_value(line, col_name, cast_type=str):
    pattern_tpl = r'{col}="([^"]*)"'
    pattern = pattern_tpl.format(col=col_name)
    match = re.search(pattern, line)
    if cast_type == int:
        null_value = 0
    else:
        null_value = None
    return cast_type(match[1]) if match is not None else null_value

def str_to_datetime(timestamp):
    f = '%Y-%m-%dT%H:%M:%S.%f'
    return datetime.strptime(timestamp, f)


def extract_tags_columns(line):
    row = {
        'Reputation': extract_column_value(line, 'Reputation', int),
        'CreationDate': extract_column_value(line, 'CreationDate', str_to_datetime),
        'LastAccessDate': extract_column_value(line, 'LastAccessDate', str_to_datetime),
        'Location': extract_column_value(line, 'Location', str),
        'Age': extract_column_value(line, 'Age', int)
    }
    return row

tags_df = db.read_text('Users.xml', encoding='utf-8', blocksize=1e8) \
.filter(lambda line: line.find('<row') >= 0) \
.map(extract_tags_columns) \
.to_dataframe().compute()

print(tags_df)

tags_df.to_csv('Users.csv')
