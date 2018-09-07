from __future__ import absolute_import
from celery.utils.log import get_task_logger
import mediacloud.api

from geoworker import mc, cliff
from geoworker.tags import CLIFF_CLAVIN_2_4_1_TAG_ID, GEONAMES_TAG_SET_NAME, GEONAMES_TAG_PREFIX, \
    CLIFF_ORGS_TAG_SET_NAME, CLIFF_PEOPLE_TAG_SET_NAME
from geoworker.celery import app

logger = get_task_logger(__name__)

# helpful to set this to False when you're debugging
POST_WRITE_BACK = True


@app.task(serializer='json', bind=True)
def geocode_from_story_text(self, story):
    # Take in a story with sentences and tag it with labels based on what the model says
    try:
        results = cliff.parse_text(story['story_text'])
        if results['status'] == cliff.STATUS_OK:
            _post_geo_tags_from_results(story, results)
            _post_entity_tags_from_results(story, results)
    except Exception as e:
        logger.exception(u"Exception - something bad happened")
        raise self.retry(exc=e)


def _post_entity_tags_from_results(story, results):
    # Add tags for people
    people_tags = []
    for person in results['results']['people']:
        people_tags.append(mediacloud.api.StoryTag(story['stories_id'], tag_set_name=CLIFF_PEOPLE_TAG_SET_NAME, tag_name=person['name']))
        logger.debug(u"  person: {} x {}".format(person['name'], person['count']))
    # Add tags for orgs
    org_tags = []
    for org in results['results']['organizations']:
        org_tags.append(mediacloud.api.StoryTag(story['stories_id'], tag_set_name=CLIFF_ORGS_TAG_SET_NAME, tag_name=org['name']))
        logger.debug(u"  org: {} x {}".format(org['name'], org['count']))
    if POST_WRITE_BACK:
        if len(people_tags) > 0:
            results = mc.tagStories(people_tags, clear_others=True)
            if results['success'] != 1:
                logger.error(u"  Tried to push {} people tags to story {}, but only got no success".format(
                    len(people_tags), story['stories_id']))
            else:
                logger.info(u"Story {}: {} people tags".format(story['stories_id'], len(people_tags)))
        if len(org_tags) > 0:
            results = mc.tagStories(org_tags, clear_others=True)
            if results['success'] != 1:
                logger.error(u"  Tried to push {} org tags to story {}, but only got no success".format(
                    len(org_tags), story['stories_id']))
            else:
                logger.info(u"Story {}: {} org tags".format(story['stories_id'], len(org_tags)))
    else:
        logger.info(u"  in testing mode - not sending sentence tags to MC")


def _post_geo_tags_from_results(story, results):
    # Tag the story as processed by this version of CLIFF
    geo_tags = [
        mediacloud.api.StoryTag(story['stories_id'], tags_id=CLIFF_CLAVIN_2_4_1_TAG_ID)
    ]
    # Add tags for the countries the story is about
    if 'countries' in results['results']['places']['focus']:
        for country in results['results']['places']['focus']['countries']:
            geo_tags.append(mediacloud.api.StoryTag(story['stories_id'],
                                                      tag_set_name=GEONAMES_TAG_SET_NAME,
                                                      tag_name=GEONAMES_TAG_PREFIX+str(country['id'])))
            # logger.debug("  focus country: {} on {}".format(country['name'],story['stories_id']) )
    # Add tags for the states within those countries that the story is about
    if 'states' in results['results']['places']['focus']:
        for state in results['results']['places']['focus']['states']:
            geo_tags.append(mediacloud.api.StoryTag(story['stories_id'],
                                                      tag_set_name=GEONAMES_TAG_SET_NAME,
                                                      tag_name=GEONAMES_TAG_PREFIX+str(state['id'])))
            # logger.debug("  focus state: {} on {}".format(state['name'],story['stories_id']) )
    if POST_WRITE_BACK:
        if len(geo_tags) > 0:
            results = mc.tagStories(geo_tags, clear_others=True)
            if results['success'] != 1:
                logger.error(u"  Tried to push {} story tags to story {}, but only got no success".format(
                    len(geo_tags), story['stories_id']))
            else:
                logger.info(u"Story {}: {} geo tags".format(story['stories_id'], len(geo_tags)))
    else:
        logger.info(u"  in testing mode - not sending sentence tags to MC")
