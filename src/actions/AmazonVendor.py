from src.actions.VendorClass import VendorClass
from src.entities.AmazonSellerCredentials import AmazonSellerCredentials
from src.entities.Order import Order
from src.entities.Item import Item
from src.util.common_functions import *
from src.mws.mws import Orders
from datetime import datetime
from src.util.get_logger import MyLogger

logger = MyLogger.logger


class AmazonVendor(VendorClass):

	def fetch_order_from_api(self, **kwargs):
		logger.info("Creating amazon invoice...")
		order_id = kwargs['order_id']
		hsn = kwargs['hsn']
		access_key = AmazonSellerCredentials.access_key
		secret_key = AmazonSellerCredentials.secret_key
		account_id = AmazonSellerCredentials.account_id
		region = AmazonSellerCredentials.region
		domain = AmazonSellerCredentials.domain
		uri = AmazonSellerCredentials.uri
		version = AmazonSellerCredentials.version
		auth_token = AmazonSellerCredentials.auth_token

		logger.info("Getting order info...")
		my_order = Orders(access_key, secret_key, account_id, region, auth_token=auth_token)
		resp = my_order.get_order(amazon_order_ids=[order_id])
		logger.info("Got order info...")

		the_order = resp["GetOrderResponse"]["GetOrderResult"]["Orders"]["Order"]
		if type(the_order) != list:
			the_order = [the_order]
		the_order = the_order[0]
		resp = my_order.list_order_items(order_id)

		order_items = resp["ListOrderItemsResponse"]["ListOrderItemsResult"]["OrderItems"]["OrderItem"]
		if type(order_items) != list:
			order_items = [order_items]
		hsn_code_rate_dict = read_property_file(get_dir_path() + '/properties/hsn_code_rates.properties')
		state = the_order["ShippingAddress"]["StateOrRegion"]
		cgst_rate, sgst_rate, igst_rate = get_tax_rates(hsn_code_rate_dict[hsn], "uttar pradesh", state.lower())

		total_amount = float(the_order["OrderTotal"]["Amount"])
		cnt = 1
		items_list = []
		for item_ in order_items:
			cgst_amt, sgst_amt, igst_amt = get_tax_amt(float(item_["ItemTax"]["Amount"]), "uttar pradesh", state.lower())
			item = Item()
			item.s_no = cnt
			item.desc_line1 = "Anti Bird Net"
			item.desc_line2 = get_net_size(item_["SellerSKU"])
			item.sku = item_["SellerSKU"]
			item.hsn_code = hsn
			item.qty = item_["QuantityOrdered"]
			item.rate = float(item_["ItemPrice"]["Amount"]) / float(item_["QuantityOrdered"]) + float(item_["PromotionDiscount"]["Amount"])
			item.discount = item_["PromotionDiscount"]["Amount"]
			item.cgst_rate = cgst_rate
			item.sgst_rate = sgst_rate
			item.igst_rate = igst_rate
			item.cgst_amt = cgst_amt
			item.sgst_amt = sgst_amt
			item.igst_amt = igst_amt
			items_list.append(item)
			cnt += 1

		order = Order()
		order.set_order_id(the_order["AmazonOrderId"])
		order.buyer_name = the_order["BuyerName"]
		order.invoice_date = datetime.now().strftime("%d-%b-%Y")
		order.billing_addr_line1 = the_order["ShippingAddress"]["AddressLine1"]
		try:
			order.billing_addr_line2 = the_order["ShippingAddress"]["AddressLine2"]
		except KeyError:
			order.billing_addr_line2 = ""
		try:
			order.billing_addr_line2 += ", " + the_order["ShippingAddress"]["City"]
		except KeyError:
			pass
		order.state = state
		order.state_code = ""
		order.items = items_list
		order.origin = "amazon"
		order.total_amount = total_amount
		order.amount_in_words = convert_num_to_words(total_amount)
		return order


if __name__ == '__main__':
	order_id = "407-0182849-5257958"
	avc = AmazonVendor().fetch_order_from_api(order_id=order_id, hsn="5608")
	items_arr = avc.items
	for item in items_arr:
		item_dict = vars(item)
		item_dict['order_id'] = order_id
		print(item_dict)
