from src.dao.dbConnection import MyMongoDB
from src.util.get_logger import MyLogger
import pymongo

logger = MyLogger.logger

DBOrders = MyMongoDB("orders")


def fetch_orders_for_month_from_db(start_timestamp, end_timestamp):
	orders = []
	for order in DBOrders.find({"timestamp": {'$gte': start_timestamp, '$lt': end_timestamp}}):
		DBItems = MyMongoDB("items")
		try:
			items_dict = DBItems.find({"order_id": order['order_id']}).sort("_id", pymongo.ASCENDING)
			order['items'] = [item for item in items_dict]
			orders.append(order)
		except:
			print("Did not find items in db for order id:" + order['order_id'])
			# raise ValueError("Did not find items in db for order id:" + order['order_id'])
	logger.info("Orders successfully fetched from db!")
	return orders
