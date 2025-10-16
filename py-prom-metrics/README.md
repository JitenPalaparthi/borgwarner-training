# Python → Prometheus Metrics (Zero to Scrape)

This minimal project exposes **Prometheus metrics** from a Python web app and ships with a **Docker Compose** setup that also runs Prometheus to scrape them.

## What you get

- `Flask` app with real HTTP endpoints and **/metrics** export
- Useful sample metrics: counters, gauges, histogram, summary
- Background job emitter to keep charts moving
- One-command demo with Docker Compose

## Run with Docker (recommended)

```bash
cd py-prom-metrics
docker compose up --build
```

- App: http://localhost:8000/healthz
- Simulated work: http://localhost:8000/work?ms=250
- Metrics: http://localhost:8000/metrics
- Prometheus UI: http://localhost:9090/

Prometheus is pre-configured (see `prometheus/prometheus.yml`) to scrape the app every 5s.

## Run locally (no Docker)

```bash
cd py-prom-metrics
make run-local
# or the long way:
# python3 -m venv .venv && . .venv/bin/activate
# pip install -r app/requirements.txt
# APP_NAME=py-prom-demo PORT=8000 python app/app.py
```

## Key metrics

- `app_requests_total{app,method,endpoint,http_status}` – all HTTP requests
- `app_request_latency_seconds_bucket{app,endpoint,le="..."}` – histogram buckets
- `app_inprogress_requests{app,endpoint}` – active in-flight requests
- `app_jobs_processed_total{app,status}` – background job outcomes
- `app_job_duration_seconds_count/sum` – summary (quantiles disabled by default)

Try hitting the app to generate data:

```bash
curl 'http://localhost:8000/work?ms=100'
curl 'http://localhost:8000/work?ms=500'
ab -n 200 -c 20 'http://localhost:8000/work?ms=120'   # if you have ApacheBench
```

## Example PromQL

- **RPS (per endpoint):**
  ```promql
  sum by (endpoint) (rate(app_requests_total[1m]))
  ```
- **95th percentile latency (per endpoint):**
  ```promql
  histogram_quantile(0.95, sum by (le, endpoint) (rate(app_request_latency_seconds_bucket[5m])))
  ```
- **Error rate:**
  ```promql
  sum(rate(app_requests_total{http_status!~"2.."}[5m])) / sum(rate(app_requests_total[5m]))
  ```

## Production tips

- Prefer a production WSGI server (gunicorn/uwsgi) and a reverse proxy.
- Keep `/metrics` cheap; avoid heavy work in collectors.
- Use labels **sparingly** (bounded cardinality).
- For batch/cron metrics, consider **Pushgateway** if your jobs are short-lived.
