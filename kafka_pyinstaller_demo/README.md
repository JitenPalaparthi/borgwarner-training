
# Kafka Producer/Consumer (Python) — PyInstaller-ready

This is a tiny, batteries-included example showing how to build standalone executables for a Kafka **producer** and **consumer** using **PyInstaller**. It uses the maintained pure‑Python client **kafka-python-ng**, which makes packaging easier than `confluent-kafka` (no external `librdkafka` dependency).

> Works on Windows, macOS, Linux. For Windows, use a native PowerShell/CMD shell (not WSL) when building the EXE if you want a Windows-native binary.

## Layout

```
kafka_pyinstaller_demo/
  producer.py
  consumer.py
  common.py
  requirements.txt
  .env.sample
  README.md
```

## Quick Start

1) **Install deps** (recommend a virtualenv):
```bash
python -m venv .venv && source .venv/bin/activate     # PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) **Set environment** (copy the sample and edit as needed):
```bash
cp .env.sample .env   # On Windows: copy .env.sample .env
```
Update `KAFKA_BOOTSTRAP` to your broker (e.g. `localhost:9092`), `KAFKA_TOPIC`, and optionally `KAFKA_GROUP_ID`.

3) **Run producer** (sends 10 example messages):
```bash
python producer.py
```

4) **Run consumer** (prints messages):
```bash
python consumer.py
```

## Build single-file executables with PyInstaller

1) Install PyInstaller:
```bash
pip install pyinstaller
```

2) Build:
```bash
pyinstaller --onefile --name kafka-producer producer.py
pyinstaller --onefile --name kafka-consumer consumer.py
```

Artifacts will be in the `dist/` folder:
- `dist/kafka-producer` (or `kafka-producer.exe` on Windows)
- `dist/kafka-consumer` (or `kafka-consumer.exe` on Windows)

3) Run the executables:
```bash
./dist/kafka-consumer
./dist/kafka-producer
```

> Tip: You can pass env vars at runtime (without `.env`):
```bash
KAFKA_TOPIC=mytopic ./dist/kafka-producer
```

## Notes

```bash
bin/kafka-topics.sh --alter \
  --topic demo-python-topic \
  --partitions 6 \
  --bootstrap-server localhost:9092
  ```