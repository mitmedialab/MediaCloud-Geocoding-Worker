import os
import sys
import logging
import mediacloud
from mediameter.cliff import Cliff
from raven.handlers.logging import SentryHandler
from raven.conf import setup_logging

VERSION = "0.1.0"
DEFAULT_CLIFF_PORT = 8080

# setup default file-based logging
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# set up logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("Starting up NYT Theme Worker v{}".format(VERSION))

try:
    RABBIT_MQ_URL = os.environ['RABBITMQ_URL']
    logger.info("RABBITMQ_URL: {}".format(RABBIT_MQ_URL))
except KeyError:
    logger.error("Missing RABBIT_MQ_URL environment variable")
    sys.exit()

try:
    MC_API_KEY = os.environ['MC_API_KEY']
    mc = mediacloud.api.AdminMediaCloud(MC_API_KEY)
    logger.info("MC_API_KEY: {}".format(MC_API_KEY))
except KeyError:
    logger.error("Missing MC_API_KEY environment variable")
    sys.exit()

try:
    CLIFF_URL = os.environ['CLIFF_URL']
    cliff = Cliff(CLIFF_URL, DEFAULT_CLIFF_PORT)
    logger.info("CLIFF_URL: {}".format(CLIFF_URL))
except KeyError:
    logger.error("Missing CLIFF_URL environment variable")
    sys.exit()

try:
    SENTRY_DSN = os.environ['SENTRY_DSN']
    logger.info("SENTRY_DSN: {}".format(SENTRY_DSN))
    handler = SentryHandler(SENTRY_DSN)
    handler.setLevel(logging.WARN)
    setup_logging(handler)
except KeyError:
    logger.error("Missing SENTRY_DSN environment variable")
