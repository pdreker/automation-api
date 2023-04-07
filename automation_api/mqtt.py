import os

import paho.mqtt.client as mqtt
from fastapi import FastAPI
from fastapi.logger import logger

app = FastAPI()


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class MQTTClient:
    _instance = None

    def __init__(self):
        self.client = mqtt.Client()
        # Configure the client as needed
        username = os.getenv("MQTT_USERNAME")
        password = os.getenv("MQTT_PASSWORD")
        if username and password:
            logger.info("Using MQTT credentials from environment variables")
            self.client.username_pw_set(username, password)
        else:
            logger.info("Using anonymous MQTT connection - no environment variables set")

        self.client.connect("rabbitmq", 1883, 60)
        self.client.loop_start()

    def publish(self, topic, payload):
        self.client.publish(topic, payload)

    def subscribe(self, topic, qos=0):
        self.client.subscribe(topic, qos)

    def unsubscribe(self, topic):
        self.client.unsubscribe(topic)

    def __del__(self):
        self.client.loop_stop()
        self.client.disconnect()

    def on_connect(self, client, userdata, flags, rc):
        logger.info("Connected to MQTT broker with result code %s", str(rc))
