from src.util.common_functions import get_invoice_name
from src.util.get_logger import MyLogger
from src.dao.fetch_orders_for_month_from_db import fetch_orders_for_month_from_db
from datetime import datetime
import json

logger = MyLogger.logger


class GetOrdersForMonth:
	def __init__(self, month, year):
		self.month = month
		self.year = year

	def get_orders_for_month(self):
		start_timestamp = int(datetime(self.year, self.month, 1).timestamp())
		if self.month + 1 > 12:
			end_timestamp = int((datetime(self.year + 1, 1, 1)).timestamp())
		else:
			end_timestamp = int((datetime(self.year, self.month + 1, 1)).timestamp())

		orders = fetch_orders_for_month_from_db(start_timestamp, end_timestamp)
		for order in orders:
			order['invoice_no'] = get_invoice_name(int(order['_id']))
			del order['billing_addr_line1']
			del order['billing_addr_line2']
			del order['gstin']
			del order['state_code']
			del order['_id']
			del order['amount_in_words']
		return orders


def get_orders_for_month(**kwargs):
	GOFM = GetOrdersForMonth(month=int(kwargs['month']), year=int(kwargs['year']))
	return GOFM.get_orders_for_month()


if __name__ == '__main__':
	my_list = get_orders_for_month(month="4", year="2018")
	print(json.dumps(my_list, indent=2))
