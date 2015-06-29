from pymongo import MongoClient
from bson import ObjectId
from settings import Common
# import datetime
# import sys
from twisted.python import log


class MongoModel(dict):
    collection_name = None

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.db = self.connect()
        self.collection = self.db[self.collection_name]

        if "_id" in self:
            record = self.collection.find_one({"_id": ObjectId(self["_id"])})
            for key in record:
                self[key] = record[key]

        log.msg("self: " + str(self))

    def connect(self):
        """
        Returns MongoClient connected to database provided as keyword
        argument 'database_name'.
        """

        client = MongoClient(host=Common.MONGO_HOST,
                             port=Common.MONGO_PORT)
        return client[Common.MONGO_DB]

    def save(self):
        return self.collection.save(self)
#        return self.collection.save(self)._id


class SessionModel(MongoModel):
    collection_name = "session"


class QOSProfileModel(MongoModel):
    collection_name = "qos"


class StatisticsModel(MongoModel):
    collection_name = "statistics"


class SOProfileModel(MongoModel):
    collection_name = "serveroverload"
