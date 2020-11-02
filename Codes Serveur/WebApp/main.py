import dbUtil
from ttnUtil import MessageType, Mqtt
import binascii
import time
from ast import literal_eval

# float_str = "-0b101010101"
# result = float(literal_eval(float_str))
from codecs import decode
import struct


def bin_to_float(b):
    """ Convert binary string to a float. """
    bf = int_to_bytes(int(b, 2), 8)  # 8 bytes needed for IEEE 754 binary64.
    return struct.unpack('>d', bf)[0]


def int_to_bytes(n, length):  # Helper function
    """ Int/long to byte string.

        Python 3.2+ has a built-in int.to_bytes() method that could be used
        instead, but the following works in earlier versions including 2.x.
    """
    return decode('%%0%dx' % (length << 1) % n, 'hex')[-length:]


def float_to_bin(value):  # For testing.
    """ Convert float to 64-bit binary string. """
    [d] = struct.unpack(">Q", struct.pack(">d", value))
    return '{:064b}'.format(d)


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

    # my_float = bin_to_float(binary)
    # print(my_float)
    # message_type = MessageType.Temperature
    # if message_type == MessageType.Temperature:
    #     _temperature = 215
    #     timestamp = time.time()
    #     database.add_temperature_measure_to_database(timestamp, _temperature, client)
    #
    # elif message_type == MessageType.Luminosity:
    #     luminosity = 215
    #     timestamp = time.time()
    #     database.add_luminosity_measure_to_database(timestamp, luminosity, client)


database = dbUtil.Database()

# temperatures = [10, 15, 20, 17, 14, 11, 13, 15, 0]
# for temperature in temperatures:
#     database.add_temperature_measure_to_database(time.time(), temperature, 1)
#
# for element in database.get_temperatures():
#     print(element)

mqtt_client = Mqtt(message_received_callback)
mqtt_client.listen()
