import os
from collections import OrderedDict as odict
from copy import deepcopy
import numpy as n
from pandas import DataFrame as pdf,read_sql
import pandas_datareader as pdr
from yahoo_fin import stock_info as yfi
from forex_python.converter import CurrencyRates as ccrates
from pymongo import MongoClient as mcx
import flask
import dash
import dash_core_components as dcc
import dash_html_components as htm
import dash_table as dtl