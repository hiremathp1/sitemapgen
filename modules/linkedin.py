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
from fuzzywuzzy import fuzz
from urllib.parse import urlparse
import logging

# If you want to call this file, put your token there
token = ""


def parse_response(response):
    json_reply = json.loads(response.text)
    results_list = []
    if "elements" in json_reply:
        for reply in json_reply["elements"]:
            out = {}
            if reply.get("name"):
                name = reply.get("name").get("localized")
                out['name'] = [name[k] for k in name][0]
            else:
                out['name'] = None

            locations = reply.get("locations")
            if locations:
                out['locations'] = locations
                headquarter = [l for l in locations if l["locationType"].upper(
                ) == "HEADQUARTERS" and "address" in l]
                location = locations[0] if not headquarter else headquarter[0]
                out['city'] = location["address"].get("city")
                out['state'] = location["address"].get("geographicArea")
                out['country'] = location["address"].get("country")
            out['city'] = "" if not out.get('city') else out.get('city')
            out['state'] = "" if not out.get('state') else out.get('state')
            out['country'] = "" if not out.get(
                'country') else out.get('country')

            results_list.append(out)

        return results_list


def get_sanitized_results(name, results_list):
    return sorted(results_list, key=lambda x: fuzz.ratio(name.upper(), x['name'].upper()))[::-1]


# Search methods

def organzation_from_email_domain(token, domain):
    site_url = urlparse(domain).netloc
    possible_domains = ['.'.join(site_url.split('.')[i:])
                        for i in range(len(site_url.split('.'))-1)]

    # The more likely is tested first
    if len(possible_domains) > 1:
        possible_domains[0], possible_domains[1] = possible_domains[1], possible_domains[0]

    for domain in possible_domains:
        url = f"https://api.linkedin.com/v2/organizations?q=emailDomain&emailDomain={domain}"
        headers = {
            'Authorization': f'Bearer {token}',
        }
        response = parse_response(
            requests.request("GET", url, headers=headers))
        if response:
            break
    return response


def organzation_from_vanityName(token, name):
    url = f"https://api.linkedin.com/v2/organizations?q=vanityName&vanityName={name}"
    headers = {
        'Authorization': f'Bearer {token}',
    }
    return parse_response(requests.request("GET", url, headers=headers))


def linkedin(token, info):
    """
    token: linkedin oauth2 api token
    info: {'name': ***, 'domain': site_url, }

    """
    results = []

    # Tries to see if the email domain is registered
    logging.info("Trying url as mail domain")
    results += organzation_from_email_domain(token, info['domain'])

    # Tries the two biggest words on the url as vanity Names
    if not results:
        logging.info("Trying vanity names from url")
        names = sorted(urlparse(info['domain']).netloc.split('.'), key=len)
        results += organzation_from_vanityName(token, names[-1])

    res = get_sanitized_results(info['name'], results)
    return res[0] if res else None


def test(token):
    test_urls = [
          "http://www.paterson.k12.nj.us/",
          "https://www.longbranch.k12.nj.us/Domain/12",
          "https://www.nbpschools.net/Domain/19",
          "https://www.chclc.org/knight",
          "https://www.nps.k12.nj.us/ABG/",
          "https://www.roselleschools.org/achs/",
          "https://ardena.howell.k12.nj.us/",
          "http://s6.gboe.org/",
          "http://www.jcboe.org/boe2015/",
          "http://hcstonline.org",
          "http://www.mcvsd.org/fullTime/academy-of-law.html",
          "http://cphs.hcstonline.org/",
    ]

    failed = []
    for url in test_urls:
        info = {'domain': url,
                'name': 'School'
                }
        r = linkedin(token, info)
        if r:
            print(r["name"], "|   city: ", r['city'], ", state: ", r['state'])
        else:
            failed.append(url)

    if failed:
        print("Failed on: ")
        [print("F", u) for u in failed]


if __name__ == "__main__":
    test(token)
