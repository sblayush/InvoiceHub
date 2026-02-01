from src.util.common_functions import get_invoice_name
from src.entities.Order import Order
from src.entities.Item import Item
from src.dao.dbConnection import MyMongoDB
from src.util.get_logger import MyLogger

logger = MyLogger.logger


def fetch_order_from_db(order_id, return_obj=True):
	DBOrders = MyMongoDB("orders")
	order_dict = DBOrders.find_one({"order_id": order_id})
	if not order_dict:
		raise ValueError("Did not find order in db with order id:" + order_id)
	else:
		DBItems = MyMongoDB("items")
		items_dict = DBItems.find({"order_id": order_id})
		if not items_dict:
			raise ValueError("Did not find items in db")
		else:
			items = []
			for item in items_dict:
				del item['_id']
				del item['order_id']
				if return_obj:
					items.append(Item(**item))
				else:
					items.append(item)
			invoice_no = get_invoice_name(int(order_dict["_id"]))
			del order_dict["_id"]
			del order_dict["timestamp"]
			order_dict['items'] = items
			order_dict['invoice_no'] = invoice_no
			logger.info("Order successfully fetched from db!")
			if return_obj:
				order = Order(**order_dict)
			else:
				order = order_dict
			return order
