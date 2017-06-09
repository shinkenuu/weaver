#!/usr/bin/env python3

import traceback
from datetime import datetime
from pymongo import MongoClient
import credential
import pigeon


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Warder(object, metaclass=Singleton):
    def __init__(self):
        self.access_dict = credential.get_credential(owner='weaver', subject='mongodb')
        self.mongo_client = MongoClient(self.access_dict['address'], self.access_dict['port'])

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def ward_progress(self, task_name: str, status: str, msg: str):
        """
            Log progress in MongoDB
        :param task_name: Which task is being updated
        :param status:the status to be logged 
        :param msg: the message to be logged
        :return: 
        """
        db = self.mongo_client['weaver']
        logs_collection = db.logs
        log_doc = {
            'task': str(task_name),
            'status': str(status),
            'when': datetime.utcnow(),
            'msg': str(msg)
        }
        logs_collection.insert_one(log_doc)

    def ward_error(self, task_name: str, exception: Exception):
        """
            Log error in MongoDB and send email to the White Tower (admins)
        :param task_name: Which task was running
        :param exception: The exception object
        :return: 
        """
        error_type_name = str(type(exception)).split("'")[1]
        self.ward_progress(task_name,
                           '{0}: {1}'.format(error_type_name, str(exception)),
                           traceback.extract_tb(exception.__traceback__))
        pigeon.alert_tower('{0}: {1}'.format(error_type_name, str(exception)))
