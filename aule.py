from prometheus_client import start_http_server, Counter, Gauge, Summary, Histogram, Info
from peewee import *
from time import sleep
from modules import test_metric
from plugins import url_plugin

db = SqliteDatabase('prometheus_metrics.db')
global_sleep_value = 5


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


db.connect()
db.create_tables([Service, Metric])

###
# Fake Metrics
###

if not Service.get(name='default'):
    Service.create(name='default')
if not Metric.get(belongs_to='default', name='test_metric'):
    Metric.create(
        belongs_to='default',
        name='test_metric',
        type='Gauge',
        description='This is a test metric.',
        source_type='null'
    )

###
# Metrics Service
###

# Global metric bucket
metric_tracker = {}

for metric in Metric.select():
    if metric.type == 'Counter':
        print("Counter: " + metric.name)
        metric_tracker[metric.name] = Counter(metric.name, metric.description)
    if metric.type == 'Gauge':
        print("Gauge: " + metric.name)
        metric_tracker[metric.name] = Gauge(metric.name, metric.description)
    if metric.type == 'Summary':
        print("Summary: " + metric.name)
        metric_tracker[metric.name] = Summary(metric.name, metric.description)
    if metric.type == 'Histogram':
        print("Histogram: " + metric.name)
        metric_tracker[metric.name] = Histogram(metric.name, metric.description)
    if metric.type == 'Info':
        print("Info: " + metric.name)
        metric_tracker[metric.name] = Info(metric.name, metric.description)


###
# Runtime
###


def url_update(update, url):
    metric_tracker[update].set(url_plugin.update_metric(url))


def loopy():
    print(metric_tracker)
    for update in metric_tracker:
        #metric_tracker[update].set(test_metric.update_metric())
        url_update(update, "https://www.random.org/integers/?num=1&min=1&max=99&col=1&base=10&format=plain&rnd=new")
    return True


if __name__ == '__main__':
    # Start up the server to expose metrics.
    print("Serving aule...")
    start_http_server(8000)
    while True:
        sleep(global_sleep_value)
        loopy()
