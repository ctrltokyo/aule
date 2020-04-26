# This is called by aule and updates the metric.
def update_metric():
    return super.url_update("test_metric", "https://www.random.org/integers/?num=1&min=1&max=99&col=1&base=10&format=plain&rnd=new")
