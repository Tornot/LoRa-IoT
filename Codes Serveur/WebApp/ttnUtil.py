import ttn
from enum import Enum


class Mqtt:

    def __init__(self, message_received_callback):
        app_id = "iot_arnaudaymeric_2020"
        access_key = "ttn-account-v2.2ZR7Kvt7lkJEVqDmK9QF4RCgsCX3DAmFTB7i8Oysu64"

        handler = ttn.HandlerClient(app_id, access_key)

        self.app_client = handler.application()
        self.mqtt_client = handler.data()
        self.mqtt_client.set_uplink_callback(message_received_callback)
        self.mqtt_client.set_connect_callback(connect_callback)
        self.mqtt_client.set_downlink_callback(downlink_callback)

        print(self.app_client.get())

    def listen(self):
        self.mqtt_client.connect()
        while(True):
            pass

    def get_devices(self):
        my_app = self.app_client.get()
        print(my_app)
        my_devices = self.app_client.devices()
        print(my_devices)

    def __del__(self):
        self.mqtt_client.close()


class MessageType(Enum):
    Temperature = 1,
    Luminosity = 2


def connect_callback(res, client):
    print(f"Connected RES: {res}, CLIENT: {client} ")


def downlink_callback(mid, client):
    print(f"Sent mid: {mid}, CLIENT: {client} ")
