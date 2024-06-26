from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError
from confluent_kafka import Consumer, Producer, KafkaError, TopicPartition
from confluent_kafka.admin import AdminClient, NewTopic
from typing import List, Dict, Any
import json
from hawk_tui.db_connectors.base import BaseConnection


class KafkaConnection(BaseConnection):
    def __init__(self, host: str, port: int, username: str = None, password: str = None):
        super().__init__(host, port, username, password)
        self.bootstrap_servers = f"{host}:{port}"
        self.admin_client = None
        self.consumer = None
        self.producer = None

    def connect(self):
        self.admin_client = KafkaAdminClient(bootstrap_servers=self.bootstrap_servers)
        self.consumer = KafkaConsumer(bootstrap_servers=self.bootstrap_servers)
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)
        return self.admin_client

    def is_connected(self) -> bool:
        try:
            self.admin_client.list_topics()
            return True
        except Exception:
            return False

    def close(self):
        if self.admin_client:
            self.admin_client.close()
        if self.consumer:
            self.consumer.close()
        if self.producer:
            self.producer.close()

    def list_consumer_groups(self) -> List[str]:
        return self.admin_client.list_consumer_groups()

    def describe_topic(self, topic: str) -> Dict[str, Any]:
        topic_info = self.admin_client.describe_topics([topic])[0]
        return {
            'name': topic_info.name,
            'partitions': len(topic_info.partitions),
            'replication_factor': len(topic_info.partitions[0].replicas),
            'is_internal': topic_info.is_internal,
        }

    def purge_topic(self, topic: str):
        # Create a new topic with the same name and config, effectively purging the old one
        topic_info = self.describe_topic(topic)
        self.delete_topic(topic)
        self.admin_client.create_topics([
            NewTopic(
                name=topic,
                num_partitions=topic_info['partitions'],
                replication_factor=topic_info['replication_factor']
            )
        ])

    def delete_topic(self, topic: str):
        self.admin_client.delete_topics([topic])

    def list_messages_in_topic(self, topic: str, limit: int = 100) -> List[Dict[str, Any]]:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset='earliest',
            consumer_timeout_ms=1000
        )
        messages = []
        for i, message in enumerate(consumer):
            if i >= limit:
                break
            messages.append({
                'offset': message.offset,
                'key': message.key.decode('utf-8') if message.key else None,
                'value': message.value.decode('utf-8'),
                'timestamp': message.timestamp,
            })
        consumer.close()
        return messages

    def messages_in_topic_count(self, topic: str) -> int:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset='earliest',
            consumer_timeout_ms=1000
        )
        partitions = consumer.partitions_for_topic(topic)
        total_messages = 0
        for partition in partitions:
            tp = TopicPartition(topic, partition)
            consumer.assign([tp])
            consumer.seek_to_end(tp)
            last_offset = consumer.position(tp)
            consumer.seek_to_beginning(tp)
            first_offset = consumer.position(tp)
            total_messages += last_offset - first_offset
        consumer.close()
        return total_messages

    def earliest_topic(self) -> str:
        topics = self.admin_client.list_topics()
        earliest_time = float('inf')
        earliest_topic = None
        for topic in topics:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=self.bootstrap_servers,
                auto_offset_reset='earliest',
                consumer_timeout_ms=1000
            )
            message = next(consumer)
            if message.timestamp < earliest_time:
                earliest_time = message.timestamp
                earliest_topic = topic
            consumer.close()
        return earliest_topic

    def latest_topic(self) -> str:
        topics = self.admin_client.list_topics()
        latest_time = 0
        latest_topic = None
        for topic in topics:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=self.bootstrap_servers,
                auto_offset_reset='latest',
                consumer_timeout_ms=1000
            )
            message = next(consumer)
            if message.timestamp > latest_time:
                latest_time = message.timestamp
                latest_topic = topic
            consumer.close()
        return latest_topic
