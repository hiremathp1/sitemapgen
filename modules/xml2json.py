#########################################################################
#  P N Hiremath -- 28, October of 2020                           #
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

def dynamoDbFormat(json_data):
    #TODO
    return json_data
    

import json, xmltodict
def convert(xml_dict):
    return dynamoDbFormat(json.dumps(xml_dict))


