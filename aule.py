from prometheus_client import start_http_server, Counter, Gauge, Summary, Histogram, Info

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
    name = CharField(unique=True)
    type = CharField(choices=['Counter', 'Gauge', 'Summary', 'Histogram', 'Info', 'Enum'])
    description = TextField()
    source_type = CharField(choices=['remote_sql_query', 'url'])


db.connect()
db.create_tables([Service, Metric])


###
# Metrics Service
###

# Test metrics
Service.create(name='default')
Metric.create(belongs_to="default", name='request_processing_seconds', type='Summary', description='Time spent processing request')

# Global metric bucket
metric_tracker = []

for metric in Metric.select():
    if metric.type == 'Counter':
        print("Counter: " + metric.name)
    if metric.type == 'Gauge':
        print("Gauge: " + metric.name)
    if metric.type == 'Summary':
        print("Summary: " + metric.name)
        Summary(metric.name, metric.description)
    if metric.type == 'Histogram':
        print("Histogram: " + metric.name)


if __name__ == '__main__':
    # Start up the server to expose metrics.
    print("Serving aule...")
    start_http_server(8000)
