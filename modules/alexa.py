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
import requests
import json
from urllib.parse import urlparse
import logging

from modules.config import config

URL_GROUPS = [
"Rank",
"RankByCountry",
"UsageStats",
"AdultContent",
"Speed",
"Language",
"LinksInCount",
"SiteData",
"TrafficData",
"ContentData",
]


class alexa:

    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'Authorization': 'AWS4-HMAC-SHA256',
            'x-api-key': api_key
        }

    def process_response(self, response):
        r = json.loads(response.text)
        try:
            for key in config.alexa.key_to_store.all:
                r = r[key]
        except Exception as e:
            logging.error("Ignoring. Failed to extract key: " +
                          key + " because"+str(e))
        return r

    def _get_urlfInfo_group(self, request_domain, group):
        url = f"https://awis.api.alexa.com/api?Action=urlInfo&ResponseGroup={group}&Url={request_domain}&Output=json"
        payload = {}
        response = requests.request(
            "GET", url, headers=self.headers, data=payload)
        if config.alexa.key_to_store.urlInfo:
            i = URL_GROUPS.index(group)
            key = config.alexa.key_to_store.urlInfo[i]
            if key:
                return self.process_response(response)[key]
            else:
                return self.process_response(response)
        else:
            return self.process_response(response)


    # UrlInfo

    def urlInfo(self, domain):
        request_domain = urlparse(domain).netloc
        output = {}
        for group in URL_GROUPS:
            output[group] = self._get_urlfInfo_group(request_domain, group)
        return output


    # TrafficHistory

    def trafficHistory(self, domain, range=config.alexa.traffic_ndays):
        request_domain = urlparse(domain).netloc
        url = f"https://awis.api.alexa.com/api?Action=TrafficHistory&Range={range}&ResponseGroup=History&Url={request_domain}&Output=json"
        payload = {}
        response = requests.request(
            "GET", url, headers=self.headers, data=payload)
        if config.alexa.key_to_store.trafficHistory:
            return self.process_response(response)[config.alexa.key_to_store.trafficHistory]
        else:
            return self.process_response(response)

    # SitesLinkingIn

    def sitesLinkingIn(self, domain, count=config.alexa.results_per_page):
        request_domain = urlparse(domain).netloc
        url = f"https://awis.api.alexa.com/api?Action=SitesLinkingIn&Count={count}&ResponseGroup=SitesLinkingIn&Url={request_domain}&Output=json"
        payload = {}
        response = requests.request(
            "GET", url, headers=self.headers, data=payload)
        if config.alexa.key_to_store.sitesLinkingIn:
            return self.process_response(response)[config.alexa.key_to_store.sitesLinkingIn]
        else:
            return self.process_response(response)

