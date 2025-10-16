
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "demo-python-topic")
GROUP_ID = os.getenv("KAFKA_GROUP_ID", "demo-python-group")

# Optional
PRODUCER_COUNT = int(os.getenv("PRODUCER_COUNT", "10"))

# Security (optional) — uncomment/adjust where used if your cluster requires it
SECURITY_PROTOCOL = os.getenv("KAFKA_SECURITY_PROTOCOL")         # e.g. SASL_SSL
SASL_MECHANISM = os.getenv("KAFKA_SASL_MECHANISM")               # e.g. SCRAM-SHA-256
SASL_USERNAME = os.getenv("KAFKA_SASL_USERNAME")
SASL_PASSWORD = os.getenv("KAFKA_SASL_PASSWORD")
SSL_CAFILE = os.getenv("KAFKA_SSL_CAFILE")
SSL_CERTFILE = os.getenv("KAFKA_SSL_CERTFILE")
SSL_KEYFILE = os.getenv("KAFKA_SSL_KEYFILE")

def client_kwargs():
    """Build kwargs for kafka-python-ng KafkaClient/Producer/Consumer."""
    kwargs = {
        "bootstrap_servers": BOOTSTRAP,
        "request_timeout_ms": 30000,
        "api_version_auto_timeout_ms": 15000,
    }
    # Apply security settings if provided
    if SECURITY_PROTOCOL:
        kwargs["security_protocol"] = SECURITY_PROTOCOL
    if SASL_MECHANISM:
        kwargs["sasl_mechanism"] = SASL_MECHANISM
    if SASL_USERNAME and SASL_PASSWORD:
        kwargs["sasl_plain_username"] = SASL_USERNAME
        kwargs["sasl_plain_password"] = SASL_PASSWORD
    if SSL_CAFILE:
        kwargs["ssl_cafile"] = SSL_CAFILE
    if SSL_CERTFILE:
        kwargs["ssl_certfile"] = SSL_CERTFILE
    if SSL_KEYFILE:
        kwargs["ssl_keyfile"] = SSL_KEYFILE
    return kwargs
