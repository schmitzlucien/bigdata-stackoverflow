# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 08:12:02 2018

@author: Lucien
"""

import pandas as pd
from lxml import etree

class DataframeBuilder(object):
    def __init__(self):
        self.dfcols = ['Reputation']
        self.df = pd.DataFrame(columns=self.dfcols)
    def start(self, tag, attrib):
        if tag == 'row':
#            attribs = dict(attrib)
            newrow = pd.Series([attrib.get('Reputation',0)], index=self.dfcols)
            self.df.append(newrow, ignore_index=True)
    def end(self, tag):
        pass
    def data(self, data):
        pass
    def comment(self, text):
        pass
    def close(self):
        return self.df

callback = DataframeBuilder()

parser = etree.XMLParser(target = callback)

with open("Users.xml", "rb") as reader:
    content = reader.read()
    
df = etree.XML(content, parser)

df.head()
