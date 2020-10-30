from pymongo import MongoClient
from bson.objectid import ObjectId


class Database:

    def __init__(self):
        client = MongoClient('mongodb://localhost:27017/')
        database = client["iot_db"]
        self.sensors_collection = database["sensors"]
        self.temperature_measures_collection = database["temperatures"]
        self.luminosity_measures_collection = database["luminosity"]

    # def get(self, post_id):
    #     post = client.db.posts.find_one({'_id': ObjectId(post_id)})
    #     title = post['title']

    def add_temperature_measure_to_database(self, timestamp, temperature, sensor):
        self.temperature_measures_collection.insert_one(temperature_measure_dict(timestamp, temperature, sensor))

    def add_luminosity_measure_to_database(self, timestamp, luminosity, sensor):
        self.luminosity_measures_collection.insert_one(luminosity_measure_dict(timestamp, luminosity, sensor))

    def get_temperatures(self):
        temperatures = self.temperature_measures_collection.find()
        return temperatures


def temperature_measure_dict(timestamp, temperature, sensor):
    return {
        "timestamp": timestamp,
        "temperature": temperature,
        "sensor": sensor
    }


def luminosity_measure_dict(timestamp, luminosity, sensor):
    return {
        "timestamp": timestamp,
        "luminosity": luminosity,
        "sensor": sensor
    }
