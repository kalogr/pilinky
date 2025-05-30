import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
import logging
import json
import time

class MQTTClient:
    """
    A simple MQTT client wrapper for publishing JSON-encoded messages with timestamps.
    Supports configurable broker, topic prefix, and dry-run mode for testing.
    """

    def __init__(self, broker='localhost', port=1666, client_id="TeleinfoPublisher", dry_run=False, topic_prefix="teleinfo"):
        """
        Initialize the MQTT client.

        :param broker: Address of the MQTT broker.
        :param port: Port of the MQTT broker.
        :param client_id: Identifier for the MQTT client.
        :param dry_run: If True, don't actually publish to the broker.
        :param topic_prefix: Prefix for MQTT topics.
        """
        self.broker = broker
        self.port = port
        self.client = mqtt.Client(client_id=client_id, callback_api_version=CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.dry_run = dry_run
        self.topic_prefix = topic_prefix

    def on_connect(self, client, userdata, flags, rc):
        """
        Callback when the client connects to the MQTT broker.

        :param client: The client instance.
        :param userdata: The private user data.
        :param flags: Response flags sent by the broker.
        :param rc: Connection result.
        """
        if rc == 0:
            logging.info("Connected to MQTT Broker!")
        else:
            logging.warning(f"Failed to connect to MQTT Broker. Return code {rc}")

    def connect(self):
        """
        Connect to the MQTT broker and start the network loop.
        """
        self.client.connect(self.broker, self.port, keepalive=60)
        self.client.loop_start()

    def publish(self, topic_suffix, value):
        """
        Publish a JSON message to the specified MQTT topic.

        :param topic_suffix: The suffix to append to the topic prefix.
        :param value: The numeric value to include in the message payload.
        """
        topic = f"{self.topic_prefix}/{topic_suffix}"
        payload = {
            "value": value,
            "timestamp": int(time.time())
        }
        message = json.dumps(payload)

        if self.dry_run:
            logging.info(f"[DRY RUN] Would publish to {topic}: {message}")
            return

        result = self.client.publish(topic, message)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            logging.info(f"Published to {topic}: {message}")
        else:
            logging.warning(f"Failed to publish to {topic}: {result.rc}")
