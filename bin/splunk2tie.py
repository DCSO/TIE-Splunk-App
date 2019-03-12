# Copyright (c) 2017, 2019, DCSO GmbH

import urllib2
import json
import csv
import sys, os
import socket
import gzip
from flor import BloomFilter
import logging, logging.handlers
import splunk
from splunk.clilib import cli_common as cli

proxy_args = cli.getConfStanza('dcso_hunt_setup','proxy')

if str(proxy_args['host']):
    proxy_link = "https://{}:{}@{}:{}".format(str(proxy_args['user']),str(proxy_args['password']),str(proxy_args['host']),str(proxy_args['port']))
    proxy = urllib2.ProxyHandler({'https': proxy_link})
    auth = urllib2.HTTPBasicAuthHandler()
    opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
    urllib2.install_opener(opener)


#with open('/opt/splunk/etc/apps/dcso_ta_tie/local/config.json') as config:
#    cfg = json.load(config)
#
#    if cfg['proxy']['host']:
#        proxy_link = "https://{}:{}@{}:{}".format(cfg['proxy']['user'],cfg['proxy']['password'],cfg['proxy']['host'],cfg['proxy']['port'])
#        proxy = urllib2.ProxyHandler({'https': proxy_link})
#        auth = urllib2.HTTPBasicAuthHandler()
#        opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
#        urllib2.install_opener(opener)

# Refactor Logging?
def setup_logging():
    logger = logging.getLogger('splunk.foo')
    SPLUNK_HOME = "/opt/splunk/"

    LOGGING_DEFAULT_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log.cfg')
    LOGGING_LOCAL_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log-local.cfg')
    LOGGING_STANZA_NAME = 'python'
    LOGGING_FILE_NAME = "tie-blf.log"
    BASE_LOG_PATH = os.path.join('var', 'log', 'splunk')
    LOGGING_FORMAT = "%(asctime)s %(levelname)-s\t%(module)s:%(lineno)d - %(message)s"
    splunk_log_handler = logging.handlers.RotatingFileHandler(os.path.join(SPLUNK_HOME, BASE_LOG_PATH, LOGGING_FILE_NAME), mode='a')
    splunk_log_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
    logger.addHandler(splunk_log_handler)
    splunk.setupSplunkLogger(logger, LOGGING_DEFAULT_CONFIG_FILE, LOGGING_LOCAL_CONFIG_FILE, LOGGING_STANZA_NAME)
    return logger

def query_tie(ioc_value):
    tie_args = cli.getConfStanza('dcso_hunt_setup','tie')
    request = urllib2.Request("{}?value={}".format(str(tie_args['feed_api']),ioc_value))
    request.add_header("X-Authorization", 'bearer {}'.format(str(tie_args['token'])))
    request.add_header("Accept", 'application/json')
    contents = json.loads(urllib2.urlopen(request).read())
    return contents

def main():
    logger = setup_logging()

    if len(sys.argv) != 14:
        print "Usage: python splunk2tie.py [value] [id] [data_type] [categories] [min_severity] [max_severity] [min_confidence] [max_confidence] [updated_at] [last_seen] [families] [actors] [hotness]"
        sys.exit(1)

    value = sys.argv[1]
    id = sys.argv[2]
    data_type = sys.argv[3]
    categories = sys.argv[4]
    min_severity = sys.argv[5]
    max_severity = sys.argv[6]
    min_confidence = sys.argv[7]
    max_confidence = sys.argv[8]
    updated_at = sys.argv[9]
    last_seen = sys.argv[10]
    families = sys.argv[11]
    actors = sys.argv[12]
    hotness = sys.argv[13]

    infile = sys.stdin
    outfile = sys.stdout

    inputs = csv.DictReader(infile)
    header = inputs.fieldnames

    output = csv.DictWriter(outfile, fieldnames=inputs.fieldnames, extrasaction='ignore')
    output.writeheader()

    bf = BloomFilter()
    with gzip.open(os.path.join(os.path.dirname(__file__),'splunk.bloom'), 'rb') as f:
        bf.read(f)

    for row in inputs:
        try:
            socket.inet_aton(row['value'])
            value = row['value']+"/32"
        except:
            value = row['value']

        if bf.check(value):
            content = query_tie(value)
            for ioc in content['iocs']:
#                print ioc
                for field_name in ('categories','families','actors'):
                    ioc[field_name]='|'.join(ioc[field_name])
                if ioc['data_type'] == "IPv4":
                    ioc['value'] = ioc['value'][:-3]
                output.writerow(ioc)
        else:
            output.writerow(row)

main()
