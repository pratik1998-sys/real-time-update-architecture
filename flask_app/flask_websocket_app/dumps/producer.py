from kafka import KafkaProducer
import json
from flask_websocket_app.dumps.config import KAFKA_BROKER_URL

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda m: json.dumps(m).encode('ascii'),
    compression_type='gzip'
)
