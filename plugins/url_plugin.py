from urllib import request


def update_metric(url):
    with request.urlopen(url) as f:
        return int(f.read())
