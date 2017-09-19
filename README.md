Media Cloud Geocoding Worker
============================

A service that will pull form a queue of stories with text and tag stories with the the countries they are about
(using CLIFF-CLAVIN results)

Dev Installation
----------------

 1. `virtualenv venv` to create your virtualenv
 2. `source venv/bin/activate` - to activate your virtualenv
 3. `pip install -r requirements.txt` - to install the dependencies

### Environment Variables

Define these:
 * **RABBITMQ_URL** - `amqp://` path to your RabbitMQ server to pull jobs from
 * **MC_API_KEY** - your mediacloud API key
 * **CLIFF_URL** - URL to your installation of the CLIFF-CLAVIN geocoding service
 * **SENTRY_DSN** - DSN for logging to Sentry
 * **MONGO_URL** - URL to your mongo database (for tracking status of things)

Use
---

Test it locally by running `celery worker -A geoworker -l info`

Seed the database with a job by running `seed-db-with-query.py "QUERY_TO_RUN" STORIES_PER_FETCH`.  This can only handle 
one job at a time. For example:

```
python seed-db-with-query.py "(publish_date:[2017-07-01T00:00:00Z TO NOW]) AND (langauge:en)" 5000
```

Then setup `queue-stories-from-db-query.py` to run on a cron - it will read the DB and page through stories matching the
database config.
