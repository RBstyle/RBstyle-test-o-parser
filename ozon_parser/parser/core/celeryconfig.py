task_track_started = True
# result_persistent = True
## Broker settings.
broker_url = "amqp://localhost"
# List of modules to import when the Celery worker starts.
imports = ("parser.tasks",)

## Using the database to store task state and results.
# result_backend = "db+sqlite:///results.db"

# task_annotations = {"tasks.add": {"rate_limit": "10/s"}}
