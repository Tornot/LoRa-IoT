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


def extract_data_from_binary(binary):
    result = []
    result[0] = int(binary[0:8], 2)
    result[1] = int(binary[8:16], 2)
    result[2] = int(binary[16:24], 2)
    result[0] = result[0] << 6
    result[0] += result[1] >> 2
    result[1] = result[1] << 8
    result[1] &= 0b1111111111
    result[1] += result[2]
    return result


def message_received_callback(msg, client):
    string = msg.payload_fields[0]
    binary = get_binary(string)
    data = extract_data_from_binary(binary)



database = dbUtil.Database()

# temperatures = [10, 15, 20, 17, 14, 11, 13, 15, 0]
# for temperature in temperatures:
#     database.add_temperature_measure_to_database(time.time(), temperature, 1)
#
# for element in database.get_temperatures():
#     print(element)

mqtt_client = Mqtt(message_received_callback)
mqtt_client.listen()
