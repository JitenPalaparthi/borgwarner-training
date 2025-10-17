import os, asyncio, logging
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from aiokafka.errors import KafkaConnectionError
from .database import SessionLocal
from .models import Message

logger = logging.getLogger(__name__)

KAFKA_BROKERS = os.getenv("KAFKA_BROKERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "demo-messages")
KAFKA_RETRY_SECONDS = int(os.getenv("KAFKA_RETRY_SECONDS", "60"))  # total retry time
KAFKA_RETRY_INTERVAL = float(os.getenv("KAFKA_RETRY_INTERVAL", "1.5"))

async def ensure_topic():
    """Ensure Kafka is reachable and the topic exists, with retries."""
    deadline = asyncio.get_event_loop().time() + KAFKA_RETRY_SECONDS
    last_err = None
    while True:
        try:
            admin = AIOKafkaAdminClient(bootstrap_servers=KAFKA_BROKERS)
            await admin.start()
            try:
                topics = await admin.list_topics()
                if KAFKA_TOPIC not in topics:
                    logger.info("Creating Kafka topic %s", KAFKA_TOPIC)
                    await admin.create_topics([NewTopic(name=KAFKA_TOPIC, num_partitions=1, replication_factor=1)])
                else:
                    logger.info("Kafka topic %s already exists", KAFKA_TOPIC)
                logger.info("Kafka reachable at %s", KAFKA_BROKERS)
                return
            finally:
                await admin.close()
        except (KafkaConnectionError, OSError) as e:
            last_err = e
            if asyncio.get_event_loop().time() >= deadline:
                logger.error("Kafka not reachable after retries: %s", e)
                raise
            logger.warning("Kafka not ready yet (%s). Retrying in %.1fs ...", e, KAFKA_RETRY_INTERVAL)
            await asyncio.sleep(KAFKA_RETRY_INTERVAL)

async def get_producer():
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKERS)
    await producer.start()
    return producer

async def send_message(text: str, key: str | None = None):
    producer = await get_producer()
    try:
        await producer.send_and_wait(KAFKA_TOPIC, value=text.encode(), key=(key.encode() if key else None))
    finally:
        await producer.stop()

async def consumer_loop(stop_event: asyncio.Event):
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKERS,
        enable_auto_commit=True,
        auto_offset_reset="earliest",
        group_id="demo-consumer-group",
    )
    # retry starting the consumer similarly
    deadline = asyncio.get_event_loop().time() + KAFKA_RETRY_SECONDS
    while True:
        try:
            await consumer.start()
            logger.info("Kafka consumer started")
            break
        except (KafkaConnectionError, OSError) as e:
            if asyncio.get_event_loop().time() >= deadline:
                logger.error("Kafka consumer could not start: %s", e)
                raise
            logger.warning("Kafka consumer not ready (%s). Retrying in %.1fs ...", e, KAFKA_RETRY_INTERVAL)
            await asyncio.sleep(KAFKA_RETRY_INTERVAL)

    try:
        async with SessionLocal() as session:
            async for msg in consumer:
                m = Message(
                    text=msg.value.decode(),
                    key=(msg.key.decode() if msg.key else None),
                    partition=msg.partition,
                    offset=msg.offset,
                )
                session.add(m)
                await session.commit()
                if stop_event.is_set():
                    break
    finally:
        await consumer.stop()
        logger.info("Kafka consumer stopped")
