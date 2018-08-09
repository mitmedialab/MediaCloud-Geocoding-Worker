import os
import sys
import logging
import mediacloud
from mediameter.cliff import Cliff
from raven.handlers.logging import SentryHandler
from raven.conf import setup_logging

from geoworker.config import get_default_config, ConfigException

VERSION = "0.2.0"
SERVICE_NAME = "Geocoding Worker"

# setup default file-based logging
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# set up logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("Starting up Geocoding Worker v{}".format(VERSION))

config = get_default_config()

BROKER_URL = config.get('BROKER_URL')
logger.info("BROKER_URL: {}".format(BROKER_URL))

MC_API_KEY = config.get('MC_API_KEY')
mc = mediacloud.api.AdminMediaCloud(MC_API_KEY)
logger.info("MC_API_KEY: {}".format(MC_API_KEY))

CLIFF_URL = config.get('CLIFF_URL')
cliff = Cliff(CLIFF_URL, 8080)
logger.info("CLIFF_URL: {}".format(CLIFF_URL))

try:
    SENTRY_DSN = config.get('SENTRY_DSN')
    logger.info("SENTRY_DSN: {}".format(SENTRY_DSN))
    handler = SentryHandler(SENTRY_DSN)
    handler.setLevel(logging.WARN)
    setup_logging(handler)
except ConfigException:
    logger.info("No logging to sentry")
