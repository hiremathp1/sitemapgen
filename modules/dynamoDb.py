#########################################################################
#  P N Hiremath -- 21, December of 2020                                 #
#                                                                       #
#########################################################################
#########################################################################
#  Depends on: boto3                                                    #
#########################################################################
import boto3
import logging
from copy import copy

class dynamoDbHandler:
    def __init__(self, keys):
        self.key = keys.key_id
        self.region = keys.region
        self.secret = keys.secretKey
        self.alexa_table = keys.alexa_table
        self.linkedin_table = keys.linkedin_table
        self.sitemap_table = keys.sitemap_table
        self.ReadCapacityUnits = keys.ReadCapacityUnits
        self.WriteCapacityUnits = keys.WriteCapacityUnits
        self.initDb()

    def initDb(self):
        self.session = boto3.session.Session(
            aws_access_key_id=self.key,  aws_secret_access_key=self.secret,  region_name=self.region)
        self.db = self.session.resource('dynamodb')

    def createTable(self, name):
        logging.info("Creating " + name)
        schema = [{
            "KeyType": "HASH",
            "AttributeName": "domain"
        }]
        definitions = [{
            "AttributeName": "domain",
            "AttributeType": "S"
        }]
        table = self.db.create_table(
            TableName=name,
            KeySchema=schema,
            AttributeDefinitions=definitions,
            ProvisionedThroughput={
                'ReadCapacityUnits': self.ReadCapacityUnits,
                'WriteCapacityUnits': self.WriteCapacityUnits
            }
        )
        # Wait until the table exists.
        logging.info("Waiting for table creation")
        table.meta.client.get_waiter('table_exists').wait(TableName=name)

    def createTablesIfNotExist(self):
        existing = [tb.name for tb in self.db.tables.all()]
        if not self.alexa_table in existing:
            name = self.alexa_table
            self.createTable(name)

        if not self.linkedin_table in existing:
            name = self.linkedin_table
            self.createTable(name)

        if not self.sitemap_table in existing:
            name = self.sitemap_table
            self.createTable(name)

    def addItem(self, table, item):
        self.db.Table(table).put_item(Item=item)

    def store(self, data):
        self.createTablesIfNotExist()
        chunk = {'domain': data['domain'], 'alexaAPIdata': data['alexaAPIdata'],
                 'schoolName': data['schoolName']}
        name = self.alexa_table
        logging.info("Sending alexa data")
        self.addItem(name, chunk)

        chunk = {'domain': data['domain'], 'linkedinAPIdata':
                 data['linkedinAPIdata'], 'schoolName': data['schoolName']}
        name = self.linkedin_table
        logging.info("Sending linkeding data")
        self.addItem(name, chunk)

        chunk = {'domain': data['domain'], "schoolName": data["schoolName"], "text/content": data["text/content"], "siteMapData": data["siteMapData"]}
        name = self.sitemap_table
        logging.info("Sending sitemap")
        self.addItem(name, chunk)

