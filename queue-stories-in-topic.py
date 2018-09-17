import sys
import logging

from geoworker import mc
from geoworker.tasks import geocode_from_story_text

logger = logging.getLogger(__name__)

if len(sys.argv) != 3:
    logger.error("Please specify a topics_id and timespans_id")
    sys.exit()

topic_id = sys.argv[1]
timespans_id = sys.argv[2]
logger.info("Processing topic {}".format(topic_id))

# debug logging
topic = mc.topic(topic_id)
logger.info("  {}".format(topic['name']))
total_stories = mc.topicStoryCount(topic_id, timespans_id=timespans_id)['count']
logger.info("  {} stories".format(total_stories))

# page through stories in topic
link_id = None
more_stories = True
while more_stories:
    # grab one page of stories
    story_page = mc.topicStoryList(topic_id, timespans_id=timespans_id, link_id=link_id, limit=500)
    # now get the stories with the text
    story_ids = [str(s['stories_id']) for s in story_page['stories']]
    query = "stories_id:({})".format(" ".join(story_ids))
    stories_with_text = mc.storyList(query, text=True)
    stories_to_geocode = [s for s in stories_with_text if s['metadata']['geocoder_version'] is None]
    logger.info("  fetched {}, queueing {}".format(len(stories_with_text), len(stories_to_geocode)))
    for s in stories_to_geocode:
        geocode_from_story_text.delay(s)
    # and get ready for the next page
    if 'next' in story_page['link_ids']:
        link_id = story_page['link_ids']['next']
    else:
        more_stories = False
