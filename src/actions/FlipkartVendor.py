from src.actions.VendorClass import VendorClass
from src.entities.FlipkartSellerCredentials import FlipkartSellerCredentials
import urllib3
import json
from src.util.common_functions import *
from src.entities.Order import Order
from src.entities.Item import Item
from datetime import datetime
from src.util.get_logger import MyLogger

logger = MyLogger.logger


class FlipkartVendor(VendorClass):

	def fetch_order_from_api(self, **kwargs):
		order_id = kwargs['order_id']
		access_token = FlipkartSellerCredentials.access_token
		app_secret = FlipkartSellerCredentials.app_secret
		app_id = FlipkartSellerCredentials.app_id
		token_type = FlipkartSellerCredentials.token_type
		http = urllib3.PoolManager()

		# Getting order info
		try:
			logger.info("Getting order info...")
			r = http.request(
				'GET', 'https://api.flipkart.net/sellers/v3/shipments?orderIds=' + order_id,
				headers={'Authorization': token_type + ' ' + access_token})
			order_info = json.loads(r.data.decode('utf-8'))
			order_info = order_info["shipments"][0]
			logger.info("Got order info...")
		except Exception as e:
			raise ValueError("failure fetching order info")

		# Getting invoice info
		try:
			logger.info("Getting invoice info...")
			shipment_id = order_info["shipmentId"]
			r = http.request(
				'GET', 'https://api.flipkart.net/sellers/v3/shipments/' + shipment_id + '/invoices',
				headers={'Authorization': token_type + ' ' + access_token})
			invoice_info = json.loads(r.data.decode('utf-8'))
			invoice_info = invoice_info["invoices"][0]
			logger.info("Got invoice info...")
		except Exception as e:
			raise ValueError("failure fetching invoice info")

		# Getting shipment info
		try:
			logger.info("Getting shipment info...")
			r = http.request(
				'GET', 'https://api.flipkart.net/sellers/v3/shipments/' + shipment_id,
				headers={'Authorization': token_type + ' ' + access_token})
			shipment_info = json.loads(r.data.decode('utf-8'))
			shipment_info = shipment_info["shipments"][0]
			logger.info("Got shipment info...")
		except Exception as e:
			raise ValueError("failure fetching invoice info")

		order_items = order_info["orderItems"]
		cnt = 1
		items_list = []
		total_amount = 0

		for item_ in order_items:
			if "igstRate" in invoice_info["orderItems"][cnt - 1]["taxDetails"]:
				cgst_rate, sgst_rate = 0, 0
				igst_rate = float(invoice_info["orderItems"][cnt - 1]["taxDetails"]["igstRate"])
				tax_rate = igst_rate / 100
			else:
				cgst_rate = float(invoice_info["orderItems"][cnt - 1]["taxDetails"]["cgstRate"])
				sgst_rate = float(invoice_info["orderItems"][cnt - 1]["taxDetails"]["sgstRate"])
				igst_rate = 0
				tax_rate = (cgst_rate + sgst_rate) / 100
			qty = item_["quantity"]

			discount = float(item_["priceComponents"]["flipkartDiscount"])
			rate = item_["priceComponents"]["sellingPrice"] / (qty * (1 + tax_rate)) + discount

			item = Item()
			item.s_no = cnt
			item.desc_line1 = "Anti Bird Net"
			item.desc_line2 = get_net_size(item_["sku"])
			item.sku = item_["sku"]
			item.hsn_code = item_["hsn"]
			item.qty = qty
			item.rate = rate
			item.discount = discount
			item.cgst_rate = str(cgst_rate)
			item.sgst_rate = str(sgst_rate)
			item.igst_rate = str(igst_rate)
			item.cgst_amt = cgst_rate * rate * qty / 100
			item.sgst_amt = sgst_rate * rate * qty / 100
			item.igst_amt = igst_rate * rate * qty / 100

			items_list.append(item)
			cnt += 1
			total_amount += item_["priceComponents"]["totalPrice"]

		order = Order()
		order.set_order_id(order_id)
		order.invoice_date = datetime.now().strftime("%d-%b-%Y")
		order.buyer_name = shipment_info["billingAddress"]["firstName"] + \
			" " + shipment_info["billingAddress"]["lastName"]
		order.billing_addr_line1 = shipment_info["billingAddress"]["addressLine1"]
		try:
			order.billing_addr_line2 = shipment_info["billingAddress"]["addressLine2"] + ", " + shipment_info["billingAddress"]["city"]
		except TypeError:
			order.billing_addr_line2 = shipment_info["billingAddress"]["city"]
		order.state = shipment_info["billingAddress"]["state"]
		order.items = items_list
		order.origin = "flipkart"
		order.total_amount = total_amount
		order.amount_in_words = convert_num_to_words(total_amount)
		return order


if __name__ == '__main__':
	fvc = FlipkartVendor().fetch_order_from_api(order_id="OD211927054904711000")
	# print()
