from prometheus_client import start_http_server, Summary
from peewee import *
import datetime
import random
import time

db = SqliteDatabase('prometheus_metrics.db')

###
# SQLite Model
###


class BaseModel(Model):
    class Meta:
        database = db


class Service(BaseModel):
    name = CharField(unique=True)


class Metric(BaseModel):
    belongs_to = ForeignKeyField(Service, backref='metric')
    message = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    is_published = BooleanField(default=True)


db.connect()
db.create_tables([Service, Metric])


###
# Metrics Service
###

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    print("Serving aule...")
    start_http_server(8000)
    # Generate some requests.
    while True:
        process_request(random.random())
