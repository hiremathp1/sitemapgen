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

def map_gen():
    from modules.sitemapGen import genMap
    #genMap("https://www.haikson.com", "test.xml")
    genMap("http://www.paterson.k12.nj.us/")

def xml2json(xml):
    from modules.xml2json import convert
    convert(xml)

def alexa():
    from modules.alexa import alexa

def linkedinAPI():
    from modules.linkedin import linkedin

if __name__ == "__main__":
    #xml=map_gen()
    xml = open("sitemap.xml").readlines()
    json_data=xml2json(xml)
    print(json_data)
    #alexa()
    #linkedinAPI()

