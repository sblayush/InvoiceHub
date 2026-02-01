from src.actions.VendorClass import VendorClass
from src.util.common_functions import *
from src.entities.Order import Order
from src.entities.Item import Item
from datetime import datetime
from src.util.get_logger import MyLogger

logger = MyLogger.logger


class OtherVendor(VendorClass):

	def fetch_order_from_api(self, **inp_order):
		total_amount = 0
		items_arr = []
		for item_ in inp_order['items']:
			cgst_rate = float(item_["cgst_rate"])
			sgst_rate = float(item_["sgst_rate"])
			igst_rate = float(item_["igst_rate"])
			tax_rate = (cgst_rate + sgst_rate + igst_rate) / 100
			qty = int(item_["qty"])
			sp = float(item_["selling_price"])
			rate = sp / (1 + tax_rate)

			item_['rate'] = rate
			del item_["selling_price"]

			item = Item(**item_)
			item.cgst_amt = cgst_rate * rate * qty / 100
			item.sgst_amt = sgst_rate * rate * qty / 100
			item.igst_amt = igst_rate * rate * qty / 100

			total_amount += sp * qty
			items_arr.append(item)

		order = Order(**inp_order)
		order.invoice_date = datetime.now().strftime("%d-%b-%Y")
		order.total_amount = total_amount
		order.amount_in_words = convert_num_to_words(total_amount)
		order.items = items_arr
		return order
