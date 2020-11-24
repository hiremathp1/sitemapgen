#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#########################################################################
#  P N Hiremath -- 28, October of 2020                              #
#                                                                       #
#########################################################################
#  Description: Sitemap generator with linkedin and alexa api           #
#  integration. Takes a url as input and responds with a dynamoDb json. #
#                                                                       #
#########################################################################
#  Depends on:  requirements.txt                                        #
#                                                                       #
#########################################################################
#  License: ???                                                         #
#  https://github.com/c4software/python-sitemap                         #
#########################################################################

import argparse
import os
import json
import modules.sitemapGen as sitemapGen

parser = argparse.ArgumentParser(description='Sitemap Generator')
parser.add_argument('--skipext', action="append", default=[], required=False, help="File extension to skip")
parser.add_argument('-n', '--num-workers', type=int, default=1, help="Number of workers if multithreading")
parser.add_argument('--parserobots', action="store_true", default=False, required=False, help="Ignore file defined in robots.txt")
parser.add_argument('--debug', action="store_true", default=False, help="Enable debug mode")
parser.add_argument('--auth', action="store_true", default=False, help="Enable basic authorisation while crawling")
parser.add_argument('-v', '--verbose', action="store_true", help="Enable verbose output")
parser.add_argument('--output', action="store", default=None, help="Output to json file")
parser.add_argument('--as-index', action="store_true", default=False, required=False, help="Outputs sitemap as index and multiple sitemap files if crawl results in more than 50,000 links (uses filename in --output as name of index file)")
parser.add_argument('--exclude', action="append", default=[], required=False, help="Exclude Url if contain")
parser.add_argument('--drop', action="append", default=[], required=False, help="Drop a string from the url")
parser.add_argument('--report', action="store_true", default=False, required=False, help="Display a report")
parser.add_argument('--images', action="store_true", default=False, required=False, help="Add image to sitemap.xml (see https://support.google.com/webmasters/answer/178636?hl=en)")
parser.add_argument('--config', action="store", default=None, help="Configuration file in json format")

group = parser.add_mutually_exclusive_group()
group.add_argument('--domain', action="store", default="", help="Target domain (ex: http://www.paterson.k12.nj.us/")
group.add_argument('--input', action="store", default=None, help="File containing list of ulr's with target domains. Notice this can take very long to process.")

arg = parser.parse_args()
# Read the config file if needed
if arg.config is not None:
	try:
		config_data=open(arg.config,'r')
		config = json.load(config_data)
		config_data.close()
	except Exception as e:
		config = {}
else:
	config = {}

# Overload config with flag parameters
dict_arg = arg.__dict__
for argument in config:
	if argument in dict_arg:
		if type(dict_arg[argument]).__name__ == 'list':
			dict_arg[argument].extend(config[argument])
		elif type(dict_arg[argument]).__name__ == 'bool':
			if dict_arg[argument]:
				dict_arg[argument] = True
			else:
				dict_arg[argument] = config[argument]
		else:
			dict_arg[argument] = config[argument]
del(dict_arg['config'])

if dict_arg["domain"] == "":
	print ("You must provide a domain or a input file to use the crawler.")
	exit()

if not dict_arg["output"]:
    print("Defaulting to sitemap.json output")
    dict_arg["output"]="sitemap.json"

#TODO loop on list of input urls
# Each site is a intensive step so better do one by one instead of parallel
# processingng of multiple urls -- keep individual multithreading for each still

sitemapGen.genMap(dict_arg, arg.report)
