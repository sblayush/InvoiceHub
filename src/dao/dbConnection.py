import pymongo
from pymongo import ReturnDocument
from abc import ABC
from src.util.Singleton import Singleton
import json
from src.config.config_paths import level
from src.util.get_logger import MyLogger

logger = MyLogger.logger


class Conn(Singleton):
	_conn = None

	@staticmethod
	def get_connection():
		try:
			if not Conn._conn:
				if level == 'p':
					uri = ""
				else:
					uri = "mongodb://localhost:27017"
				Conn._conn = pymongo.MongoClient(uri)
		except Exception as e:
			logger.exception(e)
			Conn._conn = None
		return Conn._conn


class MongoDB(ABC):

	_db_name = "accounting"

	def __init__(self):
		self._conn = Conn.get_connection()
		self._db = self._conn[MongoDB._db_name]
		self._counters = self._db.counters

	def get_next_sequence_value(self, sequence_name):
		sequence_document = self._counters.find_one_and_update(
			{"_id": sequence_name},
			{'$inc': {'sequence_value': 1}},
			return_document=ReturnDocument.AFTER,
			upsert=True
		)
		if not sequence_document:
			self._counters.insert_one({"_id": sequence_name, "sequence_value": 1})
			sequence_document = self._counters.find_one({"_id": sequence_name})
		seq_val = sequence_document['sequence_value']

		return seq_val

	def _reset_sequence_value(self, sequence_name):
		sequence_document = self._counters.find_one_and_update(
			{"_id": sequence_name},
			{"$set": {"sequence_value": 0}},
			return_document=ReturnDocument.AFTER
		)
		if not sequence_document:
			self._counters.insert_one({"_id": sequence_name, "sequence_value": 0})
			sequence_document = self._counters.find_one({"_id": sequence_name})
		if sequence_document['sequence_value'] == 0:
			print("Updated counter")
		else:
			print("Error updating counter")

	def show_counter(self):
		counter = self._counters.find({})
		print([i for i in counter])


class MyMongoDB(MongoDB):

	def __init__(self, collection_name):
		super().__init__()
		self._collection_name = collection_name
		self._collection = self._db[collection_name]

	def remove_collection(self):
		result = self._collection.remove()
		print(result)

	def insert_one(self, value):
		invoice_no = self.get_next_sequence_value(self._collection_name)
		value['_id'] = invoice_no
		result = self._collection.insert_one(value)
		return result, invoice_no

	def find(self, query):
		result = self._collection.find(query)
		return result

	def find_one(self, query):
		result = self._collection.find_one(query)
		return result

	def remove(self, query):
		result = self._collection.remove(query)

	def clear_all_data(self):
		result = self._collection.delete_many({})
		return result

	def get_collection(self):
		return self._collection

	def reset_counter(self):
		self._reset_sequence_value(self._collection_name)


def make_local_db_backup():
	"""
	Important: Put level in config_properties as 't'
	:return: None
	"""

	uri = ""
	conn = pymongo.MongoClient(uri)["accounting"]

	items = conn["items"]
	orders = conn["orders"]
	counters = conn["counters"]

	counters_dict_main = [i for i in counters.find({})]
	orders_dict_main = [i for i in orders.find({})]
	items_dict_main = [i for i in items.find({})]

	DBItems = MyMongoDB("items")
	DBOrders = MyMongoDB("orders")

	print(DBItems.clear_all_data())
	print(DBOrders.clear_all_data())
	DBItems.reset_counter()
	DBOrders.reset_counter()

	DBItems.show_counter()

	for ord in orders_dict_main:
		DBOrders.insert_one(ord)

	for ite in items_dict_main:
		DBItems.insert_one(ite)

	print([i for i in DBOrders.find({"_id": 168})])
	print([i for i in DBItems.find({"_id": 168})])


if __name__ == '__main__':
	DBItems = MyMongoDB("items")
	DBOrders = MyMongoDB("orders")
	a = [i for i in DBOrders.find({"_id": 157})][0]
	print(a)
	print([i for i in DBItems.find({"order_id": a['order_id']})])
	