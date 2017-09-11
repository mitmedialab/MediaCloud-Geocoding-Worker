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

Use
---

Test it locally by running `celery worker -A geoworker -l info`

Enqueue stories using the two queue scripts.
