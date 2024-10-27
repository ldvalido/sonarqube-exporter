import json
import logging
import re
import sys
from datetime import datetime

import requests
import rfc3339

'''
Config logging handler
'''
def get_date_string(date_object):
  return rfc3339.rfc3339(date_object)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
fileName = get_date_string(datetime.now())+'_gitlab_collecter'
logPath = 'logs'
fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
fileHandler.setFormatter(logFormatter)

'''
    Avoid duplicated logs
'''
if (rootLogger.hasHandlers()):
    rootLogger.handlers.clear()
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger()

def set_dict(dict, element):
    current_value = 0
    if (element in dict):
      current_value = dict.get(element)
    current_value += 1
    dict[element] =  current_value
      
def sr_to_json(series):
    return_value = {}
    [set_dict(return_value, s) for s in series ]
    return return_value

def get_json(element, json_data):
  if element in json_data:
    return json_data[element]
  else:
    return 0

#Get data from url and convert to JSON
def get_data(url, token):
  session = requests.Session()
  session.auth = token, ''
  call = getattr(session, 'get')
  res = call(url)
  data = json.loads(res.content)
  return data

def convert(string):
    value = re.search(r'(\d+)', string)
    unit = re.search(r'([A-Z]?B)', string)

    num = int(value.group())
    unit = unit.group()
    if unit == 'B':
        return num
    num *= 1024

    if unit == 'KB':
        return num
    num *= 1024

    if unit == 'MB':
        return num
    num *= 1024

    if unit == 'GB':
        return num
    num *= 1024

    if unit == 'TB':
        return num