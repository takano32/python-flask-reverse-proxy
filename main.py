import requests
from flask import Flask, Response, redirect, request

app = Flask(__name__)
SITE_NAME = "http://httpbin.org"


def _request(req: request, url: str):
    if req.method == "GET":
        resp = requests.get(url)
        excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif req.method == "POST":
        resp = requests.post(url, data=req.form)
        excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    pass


@app.route("/", methods=["GET", "POST"])
def index():
    global SITE_NAME
    url = f"{SITE_NAME}/"
    return _request(request, url)


@app.route("/<path:path>", methods=["GET", "POST"])
def proxy(path):
    global SITE_NAME
    url = f"{SITE_NAME}/{path}"
    return _request(request, url)


if __name__ == "__main__":
    app.run(debug=True)
