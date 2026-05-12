from flask import Flask, request, jsonify
import socket
import platform
import datetime
import os

app = Flask(__name__)


# -----------------------------
# Helpers
# -----------------------------
def get_client_ip():
    """
    Get real client IP behind proxies/load balancers
    """
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0]

    return request.remote_addr


@app.route("/")
def home():
    return jsonify({
        "message": "DevOps Monitoring API",
        "status": "running"
    })


# -----------------------------
# Return sender IP
# -----------------------------
@app.route("/api/ip")
def ip():
    return jsonify({
        "your_ip": get_client_ip(),
        "timestamp": str(datetime.datetime.utcnow())
    })


# -----------------------------
# Headers endpoint
# -----------------------------
@app.route("/api/headers")
def headers():
    return jsonify(dict(request.headers))


# -----------------------------
# Health check
# -----------------------------
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "flask-api"
    })


# -----------------------------
# System Information
# -----------------------------
@app.route("/api/system")
def system_info():
    return jsonify({
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "platform_version": platform.version(),
        "python_version": platform.python_version()
    })


# -----------------------------
# Echo endpoint
# -----------------------------
@app.route("/api/echo", methods=["POST"])
def echo():
    data = request.json

    return jsonify({
        "you_sent": data,
        "from_ip": get_client_ip()
    })


# -----------------------------
# Environment variables
# -----------------------------
@app.route("/api/env")
def env():
    return jsonify({
        "environment": os.environ.get("ENV", "development")
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)