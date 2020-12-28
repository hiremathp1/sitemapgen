# LUMOS LEARNING - Sitempa tool 
Description: A simple sitemap generator that takes any url as a input and
outputs a json.

![Overview](/graph.png "Architeture") *Overview*
![Overview](/algo.png "Architeture") *Overview*

## How to install
Setup python environment and etc..
`pip install -r requirements.txt`

## Running
```
python main.py --domain http://www.nbpschools.net/
python main.py --input input.txt
```

When using a input file, the --output will specify an output folder, by default
`output/`, but you can change it like:

```
python main.py --input input.txt --output crawling_result/
```

Take a look at config.json for more options and for command line arguments use:

```
python main.py --help
```


## Testing

``` 
python main.py --test sitemap --alexa [token] -n 8

```

This will make a basic test with 8 threads and with alexa api. You can also pass alexa or linkedin to the test argument for individual tests on each of those modules.

The linkeding test is a bit different and passing threads to it will be ignored. Just pass the oauth2 token. Look on the linkedin session for more details.


``` 
python main.py --test linkedin --linkedin [AQWZz.....some long token]

```

## Advanced usage

Read a config file to set parameters:
***You can overide (or add for list) any parameters define in the config.json***

	python main.py --config config/config.json

#### Enable debug:

  ```
 python main.py --domain http://www.nbpschools.net --debug
  ```

#### Enable verbose output:

  ```
 python main.py --domain http://www.nbpschools.net --verbose
  ```


#### Enable report for print summary of the crawl:

  ```
 python main.py --domain http://www.nbpschools.net --report
  ```

#### Skip url (by extension) (skip pdf AND xml url):

  ```
 python main.py --domain http://www.nbpschools.net --skipext pdf --skipext xml
  ```

#### Drop a part of an url via regexp :

  ```
 python main.py --domain http://www.nbpschools.net --drop "id=[0-9]{5}"
  ```

#### Exclude url by filter a part of it :

  ```
 python main.py --domain http://www.nbpschools.net --exclude "action=edit"
  ```

#### Read the robots.txt to ignore some url:

  ```
 python main.py --domain http://www.nbpschools.net --parserobots
  ```

#### Multithreaded

```
 python main.py --domain http://www.nbpschools.net --num-workers 4
```

#### with basic auth
***You need to configure `username` and `password` in your `config.json` before***
```
 python main.py --domain http://www.nbpschools.net --auth
```


#### Extract Alexa Information

```
 python main.py --domain http://www.nbpschools.net --alexa [token]
```

#### Extract LinkedIn Information

##### Generate token automatically

Run the script passing your app id and secret. Remember to enable the Marketing Developer Platform product for your app. Also add "http://localhost:3000" to `Authorized redirect URLs for your app` on the App Auth page. You can change the port and pass it to the `--port` argument of the gen script. This has to be an available port on your system.  

``` 
python gen_linkeding_oath2_token.py --id YOUR_APP_ID --secret YOUR_APP_SECRET

```

Then copy the `access_token` field from the returned json. Hit ctrl+C to stop
the server. For more information of how this works read the section bellow.


##### Generate token manually

To use the linkeding api is a bit harder because we need to obtain the oauth2
token. Create an app on linkedin, go under products and give it the 'Sign in
with linkedin' product. 

Then under apps add a authorized url like this: `http://localhost:3000` and on your local machine start listening on that port with something like: `python -m http.server 3000`. This is just for printing the redirected get parameters.

Now access the url:
``` 
https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&scope=r_liteprofile&state=123456&redirect_uri=http://localhost:3000
```
Replacing YOUR_CLIENT_ID with the information on the Auth linkedin app page.
Login and allow the app to use your account. You will be redirected to your
localhost server. Copy the code that is under the 'code' GET request. You can
also see this on the url it will redirect to. The code is whatever is in
between 'code=' and &.

Now open your browser at:

``` 
https://www.linkedin.com/oauth/v2/accessToken?grant_type=authorization_code&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&code=YOUR_AUTHORIZATION_CODE&redirect_uri=http://localhost:3000
```

Replace YOUR_CLIENT_ID, YOUR_CLIENT_SECRET with the information under Auth on
the linkedin app page. YOUR_AUTHORIZATION_CODE is the code you got on the last
step. If everything goes fine and if you didn't take too long (Those codes can
expire), then you will be redirected to a json. Copy the 'access_token' code.
That's your token. Remember it is valid for 2 months only though.

##### Use it

Pass in the oauth2 token:

```
 python main.py --domain http://www.nbpschools.net --linkedin [token]
```

Please notice that some schools will simply not have a linkedin acount or do not provide their location. 

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
  --domain DOMAIN       Target domain (ex: http://www.nbpschools.net/
  --input INPUT         File containing list of ulr's with target domains. Notice this can take very long to process.

```
## Config json
Config.json ....

```json
{
  "logging" : true, // Display logging
	"debug": true, // Display Debug info?
  "loglevel" : 0, // Level of the logging (from the python logging module). The higher less details
  "logfile" : "", // Path for a file to log. Leave empty to log on stdout
  "crawler_user_agent" : "Sitemap crawler", // Browser user agent to send
  "auth_username" : "", // In case the site requires authentication
  "auth_password" : "",
	"skipext":	[ // File extensions to skip when url is found
					"pdf",
					"xml"
				],
	"parserobots": false, // Ignore urls in robotx.txt when present?
  "max_urls_per_site" : 5000, // Max of urls to save from a site in the final json. Once this amount of urls is crawled the crawler will stop. You might want to decrease this number to avoide huge json files. 
	"exclude":	[
				"action=edit"
				],

	"alexa": {
			"traffic_ndays": 31, // Range parameter in TrafficHistory: https://awis.alexa.com/developer-guide/actions
			"results_per_page": 10 // Count parameter in SitesLinkingIn: ttps://awis.alexa.com/developer-guide/actions
      "key_to_store": ["Awis", "Results", "Result", "Alexa"] // Ordered list of keys to recursively extract from API returning json
	}

}

```

You can load your api keys directly from the config.json by something like:

```
  	"api_keys": {
		"dynamoDb" : {
			"key_id": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
			"secretKey": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
			"region": "us-west-2",
			"ReadCapacityUnits": 5,
			"WriteCapacityUnits": 5,
      "alexa_table": "a",
      "linkedin_table": "l",
      "sitemap_table": "s"
		},
		"alexa": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
		"linkedin": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    }

```

This way you don't need to use the --alexa, --linkedin parameters


## DynamoDb Integration notes

If you specify a dynamoDb id and AWS secretKey on the config.json, you will
also need to tell the linkedin, alexa and sitemap tables as in the last
example. With this your database will receive the corresponding json. 

When using this API you might want to add the `--no` argument to avoid any
output json to be neeed or created on the local filesystem. This argument will
skip the final step of writing any file to the disk. Example, just running that
with all api's set on the config.json.

``` 
python main.py --domain https://www.nbpschools.net -n 20 --no
```

Will create the tables if they don't exist on dynamoDb and avoid creating
a local sitemap.json file. Don't create the tables manually, let this program
create them with the write parameters automatically. If you create you are
advised that you are likely to have problems, so if you already have a table
with the same name you specified on config.json, remove it.


