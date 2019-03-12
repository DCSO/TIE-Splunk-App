# Copyright (c) 2017, 2019, DCSO GmbH

import urllib2
import urllib
import json
import sys, os
from subprocess import call
from datetime import datetime
from splunk.clilib import cli_common as cli

#import logging, logging.handlers
#import splunk

#def setup_logging():
#    logger = logging.getLogger('splunk.foo')    
#    SPLUNK_HOME = os.environ['SPLUNK_HOME']
#    
#    LOGGING_DEFAULT_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log.cfg')
#    LOGGING_LOCAL_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log-local.cfg')
#    LOGGING_STANZA_NAME = 'python'
#    LOGGING_FILE_NAME = "python.log"
#    BASE_LOG_PATH = os.path.join('var', 'log', 'splunk')
#    LOGGING_FORMAT = "%(asctime)s %(levelname)-s\t%(module)s:%(lineno)d - %(message)s"
#    splunk_log_handler = logging.handlers.RotatingFileHandler(os.path.join(SPLUNK_HOME, BASE_LOG_PATH, LOGGING_FILE_NAME), mode='a') 
#    splunk_log_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
#    logger.addHandler(splunk_log_handler)
#    splunk.setupSplunkLogger(logger, LOGGING_DEFAULT_CONFIG_FILE, LOGGING_LOCAL_CONFIG_FILE, LOGGING_STANZA_NAME)
#    return logger

proxy_args = cli.getConfStanza('dcso_hunt_setup','proxy')

if str(proxy_args['host']):
    proxy_link = "https://{}:{}@{}:{}".format(str(proxy_args['user']),str(proxy_args['password']),str(proxy_args['host']),str(proxy_args['port']))
    proxy = urllib2.ProxyHandler({'https': proxy_link})
    auth = urllib2.HTTPBasicAuthHandler()
    opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

def query_subscription(bloomfile):
    if bloomfile['bloomfilter']['subscr_id'] == "":
        tie_args = cli.getConfStanza('dcso_hunt_setup','tie')
        TIE_TOKEN = str(tie_args["token"])
        url = '{}/{}'.format(bloomfile['bloomfilter']['bf-sub_api'],bloomfile['bloomfilter']['query_id'])
        values = {"format" : "application/bloom"}
        data = urllib.urlencode(values)
        post = urllib2.Request(url,data)
        post.add_header("Authorization", 'Bearer {}'.format(TIE_TOKEN))
        response = json.loads(urllib2.urlopen(post).read())
        bloomfile['bloomfilter']['subscr_id'] = response['subscription']['id']
        with open(os.path.join(os.path.dirname(__file__),'../local/bloom.json'), 'w') as bloominput:
            json.dump(bloomfile,bloominput)

        return bloomfile['bloomfilter']['subscr_id']
    else:
        return bloomfile['bloomfilter']['subscr_id']

 
def get_results(bloomfile, sub_id):
    tie_args = cli.getConfStanza('dcso_hunt_setup','tie')
    TIE_TOKEN = str(tie_args["token"])
    request = urllib2.Request("{}/{}/data/latest".format(bloomfile['bloomfilter']['bf-res_api'],sub_id))
    request.add_header("X-Authorization", 'bearer {}'.format(TIE_TOKEN))
    sys.stdout = open(os.path.join(os.path.dirname(__file__),'splunk.bloom'), 'w')
    sys.stdout.write(urllib2.urlopen(request).read())

def main():
#    logger = setup_logging()
    if os.path.exists(os.path.join(os.path.dirname(__file__),'../local/bloom.json')):
        with open(os.path.join(os.path.dirname(__file__),'../local/bloom.json'), 'r') as bloominput:
            bloomfile = json.load(bloominput)
    else:
        data = {"bloomfilter":{"subscr_id": "","bf-res_api":"https://tie.dcso.de/api/v1/stored-query-results","query_id":"f978be4f-1274-4f6e-8cf9-60cc3d943bdd","bf-sub_api":"https://tie.dcso.de/api/v1/stored-query-subscriptions"}}
        with open(os.path.join(os.path.dirname(__file__),'../local/bloom.json'), 'w') as bloomfile:
            json.dump(data,bloomfile)

    sub_id = str(query_subscription(bloomfile))
    get_results(bloomfile,sub_id)

if __name__ == "__main__":
    main()
