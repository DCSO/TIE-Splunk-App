# Copyright (c) 2017, 2020, DCSO GmbH

import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
import json
import csv
import sys
import argparse
import time
import os
import logging, logging.handlers

import splunk
from splunk.clilib import cli_common as cli

proxy_args = cli.getConfStanza('dcso_hunt_setup', 'proxy')
tie_args = cli.getConfStanza('dcso_hunt_setup', 'tie')
# other_args = cli.getConfStanza('dcso_hunt_setup','other')


if str(proxy_args['host']):
    proxy_link = "https://{}:{}@{}:{}".format(str(proxy_args['user']), str(proxy_args['password']),
                                              str(proxy_args['host']), str(proxy_args['port']))
    proxy = urllib.request.ProxyHandler({'https': proxy_link})
    auth = urllib.request.HTTPBasicAuthHandler()
    opener = urllib.request.build_opener(proxy, auth, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)


def setup_logging():
    logger = logging.getLogger('splunk.foo')
    SPLUNK_HOME = "/opt/splunk/"

    LOGGING_DEFAULT_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log.cfg')
    LOGGING_LOCAL_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log-local.cfg')
    LOGGING_STANZA_NAME = 'python'
    LOGGING_FILE_NAME = "tie-pingback.log"
    BASE_LOG_PATH = os.path.join('var', 'log', 'splunk')
    LOGGING_FORMAT = "%(asctime)s %(levelname)-s\t%(module)s:%(lineno)d - %(message)s"
    splunk_log_handler = logging.handlers.RotatingFileHandler(
        os.path.join(SPLUNK_HOME, BASE_LOG_PATH, LOGGING_FILE_NAME), mode='a')
    splunk_log_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
    logger.addHandler(splunk_log_handler)
    splunk.setupSplunkLogger(logger, LOGGING_DEFAULT_CONFIG_FILE, LOGGING_LOCAL_CONFIG_FILE, LOGGING_STANZA_NAME)
    return logger


def ping_back(ioc_value):
    build = ioc_value['configuration']
    post = urllib.request.Request("%s" % str(tie_args["pingback_api"]))
    post.add_header("Authorization", 'bearer {}'.format(str(tie_args["token"])))
    post.add_data("data_type=%s&value=%s&seen=%s&occurrences=%s" % (
    build['data_type'], build['value'], build['seen'], build['occurrences']))
    response = urllib.request.urlopen(post).read()
    logger.info(response)
    return response


if __name__ == "__main__":
    logger = setup_logging()
    if len(sys.argv) < 2 or sys.argv[1] != "--execute":
        print("FATAL Unsupported execution mode (expected --execute flag)", file=sys.stderr)
        sys.exit(1)
    else:
        ioc_value = json.loads(sys.stdin.read())
        ping_back(ioc_value)
