import os
import time
import random
import threading
from flask import Flask, request, jsonify
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    Summary,
    make_wsgi_app,
    REGISTRY,
)

# Register default process/platform collectors for CPU/memory, etc.
# ProcessCollector(registry=REGISTRY)
#PlatformCollector(registry=REGISTRY)

APP_NAME = os.getenv("APP_NAME", "py-prom-demo")
PORT = int(os.getenv("PORT", "8000"))

# ------------------------- Metrics -------------------------
REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total HTTP requests",
    ["app", "method", "endpoint", "http_status"],
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Latency of HTTP requests in seconds",
    ["app", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10),
)

INPROGRESS = Gauge(
    "app_inprogress_requests",
    "Number of in-progress requests",
    ["app", "endpoint"],
)

JOB_PROCESSED = Counter(
    "app_jobs_processed_total",
    "Background jobs processed",
    ["app", "status"],
)

JOB_DURATION = Summary(
    "app_job_duration_seconds",
    "Time spent processing background jobs",
    ["app"],
)

def simulate_background_jobs():
    """Continuously emit job metrics to make the dashboard interesting."""
    while True:
        with JOB_DURATION.labels(APP_NAME).time():
            # pretend a job takes 20-800 ms
            time.sleep(random.uniform(0.02, 0.8))
        status = "success" if random.random() > 0.1 else "error"
        JOB_PROCESSED.labels(APP_NAME, status).inc()
        # idle a bit before the next job
        time.sleep(random.uniform(0.1, 0.5))

bg_thread = threading.Thread(target=simulate_background_jobs, daemon=True)
bg_thread.start()

# ------------------------- Flask app -------------------------
flask_app = Flask(__name__)

@flask_app.before_request
def before():
    request._start = time.perf_counter()
    INPROGRESS.labels(APP_NAME, request.path).inc()

@flask_app.after_request
def after(response):
    try:
        latency = time.perf_counter() - getattr(request, "_start", time.perf_counter())
        REQUEST_LATENCY.labels(APP_NAME, request.path).observe(latency)
        REQUEST_COUNT.labels(APP_NAME, request.method, request.path, response.status_code).inc()
    finally:
        INPROGRESS.labels(APP_NAME, request.path).dec()
    return response

@flask_app.get("/healthz")
def healthz():
    return jsonify(status="ok", app=APP_NAME)

@flask_app.get("/work")
def do_work():
    """
    Simulate some CPU-bound or IO-bound work.
    Control duration with ?ms=number (default 150ms)
    """
    ms = request.args.get("ms", default="150")
    try:
        delay = max(0.0, float(ms) / 1000.0)
    except ValueError:
        delay = 0.150
    # pretend to "work"
    time.sleep(delay)
    # randomly do a tiny bit more to vary latency
    time.sleep(random.uniform(0, 0.03))
    return jsonify(ok=True, took_ms=int(delay * 1000))

# Mount Prometheus metrics endpoint at /metrics
metrics_app = make_wsgi_app(REGISTRY)
application = DispatcherMiddleware(flask_app, {"/metrics": metrics_app})

if __name__ == "__main__":
    # Development server (do not use in production)
    from werkzeug.serving import run_simple
    run_simple("0.0.0.0", PORT, application, use_reloader=False, use_debugger=False)
