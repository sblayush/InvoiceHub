from src.config.seller_credentials import gstin_no
import uuid


class Order:
	def __init__(
			self,
			order_id="",
			invoice_no="",
			invoice_date="",
			buyer_name="",
			billing_addr_line1="",
			billing_addr_line2="",
			state="",
			gstin=gstin_no,
			state_code="",
			items=None,
			origin="",
			total_amount=0,
			amount_in_words=""):
		self._order_id = order_id
		self.invoice_no = invoice_no
		self.invoice_date = invoice_date
		self.buyer_name = buyer_name
		self.billing_addr_line1 = billing_addr_line1
		self.billing_addr_line2 = billing_addr_line2
		self.state = state
		self.gstin = gstin
		self.state_code = state_code
		self.items = items
		self.origin = origin
		self.total_amount = total_amount
		self.amount_in_words = amount_in_words

		if order_id == "":
			self.generate_and_set_order_id()

	def generate_and_set_order_id(self):
		self._order_id = str(uuid.uuid4())

	def get_order_id(self):
		return self._order_id

	def set_order_id(self, oid):
		self._order_id = oid
