from __future__ import absolute_import
from celery.utils.log import get_task_logger
import mediacloud.api

from geoworker import mc, cliff
from geoworker.tags import CLIFF_CLAVIN_2_3_0_TAG_ID, GEONAMES_TAG_SET_NAME, GEONAMES_TAG_PREFIX
from geoworker.celery import app

logger = get_task_logger(__name__)

# helpful to set this to False when you're debugging
POST_WRITE_BACK = True


@app.task(serializer='json', bind=True)
def geocode_from_story_text(self, story):
    # Take in a story with sentences and tag it with labels based on what the model says
    try:
        results = cliff.parseText(story['story_text'])
        _post_tags_from_results(story, results)
    except Exception as e:
        logger.exception("Exception - something bad happened")
        raise self.retry(exc=e)


def _post_tags_from_results(story, results):
    if results['status'] == cliff.STATUS_OK:
        # Tag the story as processed by this version of CLIFF
        story_tags = [
            mediacloud.api.StoryTag(story['stories_id'], tags_id=CLIFF_CLAVIN_2_3_0_TAG_ID)
        ]
        # Add tags for the countries the story is about
        if 'countries' in results['results']['places']['focus']:
            for country in results['results']['places']['focus']['countries']:
                story_tags.append( mediacloud.api.StoryTag(story['stories_id'],
                                                           tag_set_name=GEONAMES_TAG_SET_NAME,
                                                           tag_name=GEONAMES_TAG_PREFIX+str(country['id'])))
                # logger.debug("  focus country: {} on {}".format(country['name'],story['stories_id']) )
        # Add tags for the states within those countries that the story is about
        if 'states' in results['results']['places']['focus']:
            for state in results['results']['places']['focus']['states']:
                story_tags.append( mediacloud.api.StoryTag(story['stories_id'],
                                                           tag_set_name=GEONAMES_TAG_SET_NAME,
                                                           tag_name=GEONAMES_TAG_PREFIX+str(state['id'])) )
                # logger.debug("  focus state: {} on {}".format(state['name'],story['stories_id']) )
        if POST_WRITE_BACK:
            if len(story_tags)>0:
                results = mc.tagStories(story_tags, clear_others=True)
                if results['success'] != 1:
                    logger.error("  Tried to push {} story tags to story {}, but only got no success".format(
                        len(story_tags),story['stories_id']))
        else:
            logger.info("  in testing mode - not sending sentence tags to MC")
