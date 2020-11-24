# Sitemap Generator
Description: A simple sitemap generator that takes any url as a input and
outputs a json.

![Overview](/graph.png "Architeture") *Overview*

## How to install
Setup python environment and etc..
`pip install -r requirements.txt`

## Running
```
python main.py --domain http://www.paterson.k12.nj.us/
python main.py --input input.txt
```

Take a look at config.json for more options and for command line arguments use:

```
python main.py --help
```
## Advanced usage

Read a config file to set parameters:
***You can overide (or add for list) any parameters define in the config.json***

	python main.py --config config/config.json

#### Enable debug:

  ```
 python main.py --domain http://www.paterson.k12.nj.us --debug
  ```

#### Enable verbose output:

  ```
 python main.py --domain http://www.paterson.k12.nj.us --verbose
  ```


#### Enable report for print summary of the crawl:

  ```
 python main.py --domain http://www.paterson.k12.nj.us --report
  ```

#### Skip url (by extension) (skip pdf AND xml url):

  ```
 python main.py --domain http://www.paterson.k12.nj.us --skipext pdf --skipext xml
  ```

#### Drop a part of an url via regexp :

  ```
 python main.py --domain http://www.paterson.k12.nj.us --drop "id=[0-9]{5}"
  ```

#### Exclude url by filter a part of it :

  ```
 python main.py --domain http://www.paterson.k12.nj.us --exclude "action=edit"
  ```

#### Read the robots.txt to ignore some url:

  ```
 python main.py --domain http://www.paterson.k12.nj.us --parserobots
  ```

#### Multithreaded

```
 python main.py --domain http://www.paterson.k12.nj.us --num-workers 4
```

#### with basic auth
***You need to configure `username` and `password` in your `config.json` before***
```
 python main.py --domain http://www.paterson.k12.nj.us --auth
```

## Help
```

usage: python main.py [-h] [--skipext SKIPEXT] [-n NUM_WORKERS] [--parserobots] [--debug] [--auth] [-v] [--output OUTPUT] [--as-index]
               [--exclude EXCLUDE] [--drop DROP] [--report] [--images] [--config CONFIG] [--domain DOMAIN | --input INPUT]


optional arguments:
  -h, --help            show this help message and exit
  --skipext SKIPEXT     File extension to skip
  -n NUM_WORKERS, --num-workers NUM_WORKERS
                        Number of workers if multithreading
  --parserobots         Ignore file defined in robots.txt
  --debug               Enable debug mode
  --auth                Enable basic authorisation while crawling
  -v, --verbose         Enable verbose output
  --output OUTPUT       Output to json file
  --as-index            Outputs sitemap as index and multiple sitemap files if crawl results in more than 50,000 links (uses
                        filename in --output as name of index file)
  --exclude EXCLUDE     Exclude Url if contain
  --drop DROP           Drop a string from the url
  --report              Display a report
  --config CONFIG       Configuration file in json format
  --domain DOMAIN       Target domain (ex: http://www.paterson.k12.nj.us/
  --input INPUT         File containing list of ulr's with target domains. Notice this can take very long to process.

```
## Config json
Config.json ....
  * TODO - Explain all

```json
{
  "logging" : true,
	"debug":true,
  "loglevel" : 0,
  "logfile" : "",
  "crawler_user_agent" : "Sitemap crawler",
  "auth_username" : "",
  "auth_password" : "",
	"skipext":	[
					"pdf",
					"xml"
				],
	"parserobots":false,
  "max_urls_per_site" : 50000,
	"exclude":	[
				"action=edit"
				]


}

```

``` Copyright
This Document belongs to Lumos Learning and developed by P N Hiremath

```
