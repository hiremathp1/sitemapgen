import json
from collections import namedtuple
from json import JSONEncoder

def customStudentDecoder(studentDict):
    return namedtuple('X', studentDict.keys())(*studentDict.values())

try:
    config = json.loads(open("config.json").read(), object_hook=customStudentDecoder)
except Exception as e:
    print(e)
    print("Your config.json has invalid syntax!")
    exit(1)

if config.logging:
    import logging
    logging.basicConfig(filename=config.logfile, level=config.loglevel)


crawler_user_agent = config.crawler_user_agent
max_urls_per_site = config.max_urls_per_site

username = config.auth_username
password = config.auth_password