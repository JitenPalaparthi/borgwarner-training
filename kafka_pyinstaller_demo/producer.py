
import json
import signal
import sys
import time
import logging
from datetime import datetime

from kafka import KafkaProducer
from common import TOPIC, PRODUCER_COUNT, client_kwargs

log = logging.getLogger("producer")

shutdown = False
def _sig_handler(signum, frame):
    global shutdown
    log.info("Signal %s received, shutting down...", signum)
    shutdown = True

for s in (signal.SIGINT, signal.SIGTERM):
    signal.signal(s, _sig_handler)

def main():
    kwargs = client_kwargs()
    log.info("Connecting producer to %s", kwargs.get("bootstrap_servers"))
    producer = KafkaProducer(
        **kwargs,
        value_serializer=lambda d: json.dumps(d).encode("utf-8"),
        acks="all",
        linger_ms=10,
        retries=5,
    )

    sent = 0
    for i in range(PRODUCER_COUNT):
        if shutdown:
            break
        payload = {
            "i": i,
            "ts": datetime.utcnow().isoformat() + "Z",
            "msg": f"hello from python producer #{i}",
        }
        fut = producer.send(TOPIC, value=payload)
        metadata = fut.get(timeout=10)
        log.info("Sent -> topic=%s partition=%s offset=%s", metadata.topic, metadata.partition, metadata.offset)
        sent += 1
        time.sleep(2.)

    log.info("Flushing producer...")
    producer.flush(timeout=10)
    log.info("Done. Total sent: %s", sent)
    producer.close()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.exception("Producer error: %s", e)
        sys.exit(1)
