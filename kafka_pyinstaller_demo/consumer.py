
import json
import signal
import sys
import logging

from kafka import KafkaConsumer
from common import TOPIC, GROUP_ID, client_kwargs

log = logging.getLogger("consumer")

shutdown = False
def _sig_handler(signum, frame):
    global shutdown
    log.info("Signal %s received, shutting down...", signum)
    shutdown = True

for s in (signal.SIGINT, signal.SIGTERM):
    signal.signal(s, _sig_handler)

def main():
    kwargs = client_kwargs()
    log.info("Connecting consumer to %s", kwargs.get("bootstrap_servers"))
    consumer = KafkaConsumer(
        TOPIC,
        **kwargs,
        group_id=GROUP_ID,
        enable_auto_commit=True,
        auto_offset_reset="earliest",
        value_deserializer=lambda b: json.loads(b.decode("utf-8")),
        ##consumer_timeout_ms=0,  # block forever until messages or signal
    )

    for msg in consumer:
        if shutdown:
            break
        log.info("Got: partition=%s offset=%s key=%s value=%s", msg.partition, msg.offset, msg.key, msg.value)

    log.info("Closing consumer...")
    consumer.close()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.exception("Consumer error: %s", e)
        sys.exit(1)
