from src.dao.dbConnection import MyMongoDB
from src.util.common_functions import get_invoice_name
from src.util.get_logger import MyLogger
from datetime import datetime
import copy

logger = MyLogger.logger


def write_order_to_db(order):
	DBOrders = MyMongoDB("orders")
	DBItems = MyMongoDB("items")
	items_arr = copy.deepcopy(order.items)
	order_dict = copy.deepcopy(vars(order))
	order_dict['order_id'] = order_dict['_order_id']
	order_dict['timestamp'] = int(datetime.now().timestamp())
	del order_dict['items']
	del order_dict['_order_id']
	result, invoice_no = DBOrders.insert_one(order_dict)
	if result.acknowledged:
		order.invoice_no = get_invoice_name(int(invoice_no))
		logger.info("Order written to db status: " + str(result.acknowledged))
		for item in items_arr:
			item_dict = vars(item)
			item_dict['order_id'] = order.get_order_id()
			result, _ = DBItems.insert_one(item_dict)
			if result.acknowledged:
				logger.info("Item written to db status: " + str(result.acknowledged))
			else:
				raise ValueError("Could not write Item to DB")

	else:
		raise ValueError("Could not write Order to DB")
