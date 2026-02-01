class Item:
	def __init__(
			self,
			s_no="",
			desc_line1="",
			desc_line2="",
			hsn_code="",
			qty="",
			rate="",
			discount="",
			cgst_rate="",
			sgst_rate="",
			igst_rate="",
			cgst_amt="",
			sgst_amt="",
			igst_amt="",
			sku=""):
		self.s_no = s_no
		self.desc_line1 = desc_line1
		self.desc_line2 = desc_line2
		self.hsn_code = hsn_code
		self.qty = qty
		self.rate = rate
		self.discount = discount
		self.cgst_rate = cgst_rate
		self.sgst_rate = sgst_rate
		self.igst_rate = igst_rate
		self.cgst_amt = cgst_amt
		self.sgst_amt = sgst_amt
		self.igst_amt = igst_amt
		self.sku = sku
