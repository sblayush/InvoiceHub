from src.util.get_logger import MyLogger
from src.dao.fetch_order_from_db import fetch_order_from_db

logger = MyLogger.logger


class EditInvoice:
	def __init__(self):
		pass

	def get_invoice_from_db(self, order_id):
		order = fetch_order_from_db(order_id, return_obj=False)
		return order
