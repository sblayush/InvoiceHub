import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)).replace('\\', '/'))
sys.path.append(parent_dir)

import pymongo
from datetime import datetime
from src.config.config_paths import backup_op_path
from src.util.common_functions import create_dir, does_dir_exist
import json
from src.util.get_logger import MyLogger

logger = MyLogger.logger


class TakeLocalBackup:
	def __init__(self):
		self.op_path = backup_op_path + '/' + self._get_date_string()
		if not does_dir_exist(self.op_path):
			create_dir(self.op_path)

	def _get_date_string(self):
		return datetime.now().strftime("%d-%b-%Y")

	def make_local_file_backup(self):
		uri = ""
		conn = pymongo.MongoClient(uri)["accounting"]

		items = conn["items"]
		orders = conn["orders"]
		counters = conn["counters"]

		counters_dict_main = [i for i in counters.find({})]
		orders_dict_main = [i for i in orders.find({})]
		items_dict_main = [i for i in items.find({})]

		with open(self.op_path+'/counter.json', 'w') as f:
			json.dump(counters_dict_main, f, indent=2)
			logger.info("Counters backup done!")

		with open(self.op_path+'/items.json', 'w') as f:
			json.dump(items_dict_main, f, indent=2)
			logger.info("Items backup done!")

		with open(self.op_path+'/orders.json', 'w') as f:
			json.dump(orders_dict_main, f, indent=2)
			logger.info("Orders backup done!")


def take_local_file_backup():
	TakeLocalBackup().make_local_file_backup()

take_local_file_backup()
