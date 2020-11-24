#!/usr/bin/python3

#########################################################################
#  Matheus Fillipe -- 6, November of 2020                               #
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
from modules.sitemapGen import genMap
import sys

if __name__ == '__main__':
    genMap(sys.argv[1])
