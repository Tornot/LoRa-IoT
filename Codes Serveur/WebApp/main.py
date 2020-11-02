import dbUtil
from ttnUtil import MessageType, Mqtt
import binascii
import time
from ast import literal_eval


def get_binary(string):
    out_string = ""
    received_bytes = string[:-1].split('/')
    for incomplete_binary in received_bytes:
        number_of_zeros_to_add = 8 - len(incomplete_binary)
        complete_binary = ''.join('0' for i in range(number_of_zeros_to_add)) + incomplete_binary
        out_string += complete_binary

    return out_string


def message_received_callback(msg, client):
    print(msg)
    string = msg.payload_fields[0]
    binary = get_binary(string)
    print(binary)


database = dbUtil.Database()

# temperatures = [10, 15, 20, 17, 14, 11, 13, 15, 0]
# for temperature in temperatures:
#     database.add_temperature_measure_to_database(time.time(), temperature, 1)
#
# for element in database.get_temperatures():
#     print(element)

mqtt_client = Mqtt(message_received_callback)
mqtt_client.listen()
