from kafka import KafkaProducer, KafkaConsumer
import json
import logging
from typing import Dict, Any, Callable
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka topic definitions
TOPICS = {
    'CUSTOMER_MESSAGES': 'customer-messages',
    'AGENT_RESPONSES': 'agent-responses',
    'ESCALATIONS': 'escalations',
    'CONVERSATION_UPDATES': 'conversation-updates'
}

class FTEKafkaProducer:
    def __init__(self):
        self.producer = None

    def start(self):
        """Initialize the Kafka producer"""
        try:
            kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

            self.producer = KafkaProducer(
                bootstrap_servers=kafka_bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                acks=1,  # Wait for leader to acknowledge
                retries=3,
                linger_ms=5,  # Small delay to batch messages
                batch_size=16384
            )
            logger.info("Kafka producer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka producer: {e}")
            raise

    def send_message(self, topic: str, message: Dict[str, Any], key: str = None):
        """Send a message to a Kafka topic"""
        if not self.producer:
            self.start()

        try:
            future = self.producer.send(topic, value=message, key=key)
            result = future.get(timeout=10)  # Wait for delivery confirmation
            logger.info(f"Message sent to topic {topic}, partition {result.partition}, offset {result.offset}")
            return result
        except Exception as e:
            logger.error(f"Failed to send message to {topic}: {e}")
            raise

    def close(self):
        """Close the Kafka producer"""
        if self.producer:
            self.producer.close()
            logger.info("Kafka producer closed")

class FTEKafkaConsumer:
    def __init__(self):
        self.consumer = None

    def start(self, topics: list):
        """Initialize the Kafka consumer"""
        try:
            kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

            self.consumer = KafkaConsumer(
                *topics,
                bootstrap_servers=kafka_bootstrap_servers,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                key_deserializer=lambda k: k.decode('utf-8') if k else None,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='fte-consumer-group'
            )
            logger.info(f"Kafka consumer initialized for topics: {topics}")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka consumer: {e}")
            raise

    def consume_messages(self, callback: Callable[[Dict], None]):
        """Start consuming messages and process them with callback"""
        try:
            for message in self.consumer:
                try:
                    logger.info(f"Consumed message from {message.topic}/{message.partition} at offset {message.offset}")
                    callback(message.value)
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    continue
        except KeyboardInterrupt:
            logger.info("Consumer interrupted by user")
        except Exception as e:
            logger.error(f"Consumer error: {e}")
        finally:
            self.close()

    def close(self):
        """Close the Kafka consumer"""
        if self.consumer:
            self.consumer.close()
            logger.info("Kafka consumer closed")
