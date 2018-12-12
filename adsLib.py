import os
from collections import OrderedDict as odict
from datetime import datetime as dtm,timedelta
from copy import deepcopy
import numpy as n
from pandas import DataFrame as pdf,read_sql
from pandas_datareader import data as pdr
from yahoo_fin import stock_info as yfi
from forex_python.converter import CurrencyRates as ccrates
from pymongo import MongoClient as mcx
from flask import Flask
import dash
import dash_core_components as dcc
import dash_html_components as htm
import dash_table as dtl
from dash.dependencies import Input, Output
from plotly import graph_objs as go