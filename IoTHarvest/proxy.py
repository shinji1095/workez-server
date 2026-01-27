from flask import Flask, request, Response, send_from_directory
from dotenv import load_dotenv
import requests
import os

# --------------------------------
# Setup
# --------------------------------
load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
API = os.getenv("API")
BASE = os.path.join(os.getcwd(), "public")

if not ACCESS_TOKEN:
    raise RuntimeError("ACCESS_TOKEN missing from .env")

app = Flask(__name__)

print("✔ Proxy running")
print("✔ API:", API)
print("✔ Token loaded:", bool(ACCESS_TOKEN))
print("✔ Public dir:", BASE)

# --------------------------------
# Page Routes
# --------------------------------
def serve_page(name):
    return send_from_directory(
        os.path.join(BASE, "pages"),
        f"{name}.html"
    )

@app.route("/")
@app.route("/index")
def index():
    return serve_page("index")

@app.route("/harvest")
def harvest():
    return serve_page("harvest")

@app.route("/analytics")
def analytics():
    return serve_page("analytics")

@app.route("/revenue")
def revenue():
    return serve_page("revenue")

@app.route("/users")
def users():
    return serve_page("users")

@app.route("/targets")
def targets():
    return serve_page("targets")

@app.route("/defects")
def defects():
    return serve_page("defects")

# --------------------------------
# Static Files
# --------------------------------
@app.route("/css/<path:filename>")
def css(filename):
    return send_from_directory(os.path.join(BASE, "css"), filename)

@app.route("/js/<path:filename>")
def js(filename):
    return send_from_directory(os.path.join(BASE, "js"), filename)

# --------------------------------
# API Proxy (TOKEN INJECTED HERE)
# --------------------------------
@app.route("/api/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def proxy(path):

    if request.method == "OPTIONS":
        return Response(
            status=204,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Authorization, Content-Type",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            }
        )

    print("→ API:", request.method, path)

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": request.headers.get("Accept", "*/*")
    }

    upstream = requests.request(
        method=request.method,
        url=f"{API}/{path}",
        params=request.args,
        headers=headers,
        data=request.get_data(),
        stream=True,
        allow_redirects=False,
    )

    excluded = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection"
    ]

    response_headers = [
        (k, v) for k, v in upstream.headers.items()
        if k.lower() not in excluded
    ]

    response_headers.append(("Access-Control-Allow-Origin", "*"))

    return Response(
        upstream.iter_content(chunk_size=8192),
        status=upstream.status_code,
        headers=response_headers
    )

# --------------------------------
# Run
# --------------------------------
if __name__ == "__main__":
    app.run(port=5500, debug=True)
