#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#########################################################################
#  P N Hiremath -- 28, October of 2020                                  #
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
#                                                                       #
#########################################################################

iimport argparse
import os, sys
import json
import modules.sitemapGen as sitemapGen
from modules.alexa import alexa


parser = argparse.ArgumentParser(description='Sitemap Generator')
parser.add_argument('--skipext', action="append", default=[],
                    required=False, help="File extension to skip")
parser.add_argument('-n', '--num-workers', type=int, default=1,
                    help="Number of workers if multithreading")
parser.add_argument('--parserobots', action="store_true", default=False,
                    required=False, help="Ignore file defined in robots.txt")
parser.add_argument('--debug', action="store_true",
                    default=False, help="Enable debug mode")
parser.add_argument('--auth', action="store_true", default=False,
                    help="Enable basic authorisation while crawling")
parser.add_argument('-v', '--verbose', action="store_true",
                    help="Enable verbose output")
parser.add_argument('--output', action="store",
                    default=None, help="Output to json file")
parser.add_argument('--no', action="store_true",
                    default=False, help="No output, Ommit output.")
parser.add_argument('--as-index', action="store_true", default=False, required=False,
                    help="Outputs sitemap as index and multiple sitemap files if crawl results in more than 50,000 links (uses filename in --output as name of index file)")
parser.add_argument('--exclude', action="append", default=[],
                    required=False, help="Exclude Url if contain")
parser.add_argument('--drop', action="append", default=[],
                    required=False, help="Drop a string from the url")
parser.add_argument('--report', action="store_true",
                    default=False, required=False, help="Display a report")
parser.add_argument('--images', action="store_true", default=False, required=False,
                    help="Add image to sitemap.xml (see https://support.google.com/webmasters/answer/178636?hl=en)")
parser.add_argument('--linkedin', action="store", default=None, required=False,
                    help="Extracts and adds linkedin data to output result")
parser.add_argument('--alexa', action="store", default=None, required=False,
                    help="Extracts and adds alexa traffic data to output result")
parser.add_argument('--config', action="store", default=None,
                    help="Use a different configuration json file by specifying the path")
parser.add_argument('--test', choices=["alexa", "linkedin", "sitemap"], action="store", default=None, required=False,
                    help="Test modules separately")

group = parser.add_mutually_exclusive_group()
group.add_argument('--domain', action="store", default="",
                   help="Target domain (ex: http://www.paterson.k12.nj.us/")
group.add_argument('--input', action="store", default=None,
                   help="File containing list of ulr's with target domains. Notice this can take very long to process.")


arg = parser.parse_args()
# Read the config file if needed
if arg.config is not None:
    try:
        config_data = open(arg.config, 'r')
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


# Tests

if dict_arg['test']:
    test_domain = "https://www.haikson.com"
    print("TESTING", dict_arg["test"].upper(), "on ", test_domain)

    if dict_arg['test']=="sitemap":
        dict_arg["domain"] = test_domain
        dict_arg["output"] = "test.json"
        del(dict_arg['test'])
        sitemapGen.genMap(dict_arg, arg.report)
        print("Saved at", dict_arg["output"])

    elif dict_arg['test']=="alexa":
        if dict_arg["alexa"]:
            alx = alexa(dict_arg["alexa"])
            print(alx.urlInfo(test_domain))
            print(alx.trafficHistory(test_domain))
            print(alx.sitesLinkingIn(test_domain))
        else:
            print("You need to pass in the alexa api key with the --alexa argument")

    elif dict_arg['test']=="linkedin":
        if dict_arg["linkedin"]:
            from modules.linkedin import test
            test(dict_arg["linkedin"])
        else:
            print("You need to pass in the linkedin api key with the --linkedin argument")
    sys.exit(0)

del(dict_arg['test'])


if dict_arg['no']:
    print("Ommiting file output")
if not dict_arg["output"] and not dict_arg["input"]:
    if not dict_arg['no']:
        print("Defaulting to sitemap.json output")
    dict_arg["output"] = "sitemap.json"
elif not dict_arg["output"] and dict_arg["input"]:
    if not dict_arg['no']:
        print("Defaulting to sitemap folder output")
    dict_arg["output"] = "sitemap"

if not dict_arg["alexa"]:
    del dict_arg["alexa"]
if not dict_arg["linkedin"]:
    del dict_arg["linkedin"]

if dict_arg["input"]:
    import validators
    filename = dict_arg["input"]
    output = dict_arg["output"]
    if os.path.isfile(filename):
        for link in open(filename).readlines():
            if validators.url(link) == True:
                dict_arg["domain"] = link
                dict_arg["output"] = output + "/" + link + ".json"
                try:
                    sitemapGen.genMap(dict_arg, arg.report)
                except Exception as e:
                    print("IGNORING URL: ", link, "\nBecause: ", e)
            else:
                print("IGNORING INVALID URL: ", link, " !!!")
    else:
        print("Input file not found!")
else:
    sitemapGen.genMap(dict_arg, arg.report)

