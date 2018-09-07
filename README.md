Media Cloud Geocoding Worker
============================

A service that will pull form a queue of stories with text and tag stories with the the countries they are about
(using CLIFF-CLAVIN results)

Dev Installation
----------------

Install redis. Then:

 1. `virtualenv venv` to create your virtualenv
 2. `source venv/bin/activate` - to activate your virtualenv
 3. `pip install -r requirements.txt` - to install the dependencies

### Configuration

Define the settings you need to in `app.config`, based on the template in there.

Use
---

Run the workers in one window by doing: `celery worker -A geoworker -l info`.

### Tagging all stories in a Topic

In another window start up the story fetcher with `python queue-stories-in-topic.py 1234` (where 1234 is the id 
of the topic you want to process),

### Tagging stories matching a query

Fill in the `app.config` with your query and filter_query, then run `queue-stories-from-query` from a cronjob.
