#!/usr/bin/env python

import traceback
from datetime import datetime
from pymongo import MongoClient
import credentials
import pigeon


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Warder(object, metaclass=Singleton):
    def __init__(self):
        self.credential = credentials.credentials_dict['mongodb']
        self.mongo_client = MongoClient(self.credential.ipAddress, self.credential.port)

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def ward_progress(self, task_name, status, msg):
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

    def ward_error(self, task_name, exception):
        """
            Log error in MongoDB and send email to the White Tower (admins)
        :param task_name: Which task was running
        :param exception: The exception object
        :return: 
        """
        self.ward_progress(task_name, 'error', traceback.extract_tb(exception.__traceback__))
        pigeon.alert_tower('{}\n\n{}'.format(traceback.extract_stack(),
                                             traceback.extract_tb(exception.__traceback__)))
