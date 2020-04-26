from urllib import request


def update_metric():
    try:
        with request.urlopen(
                "https://www.random.org/integers/?num=1&min=1&max=99&col=1&base=10&format=plain&rnd=new") as f:
            return f.read(100).decode('utf-8')
    finally:
        return 0
