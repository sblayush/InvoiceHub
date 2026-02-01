from abc import ABC, abstractmethod
from openpyxl import load_workbook
from src.util.common_functions import does_dir_exist, create_dir
from src.dao.fetch_order_from_db import fetch_order_from_db
from src.dao.write_order_to_db import write_order_to_db
import src.config.config_paths as config_paths
from src.util.get_logger import MyLogger

logger = MyLogger.logger


class VendorClass(ABC):
	
	@abstractmethod
	def fetch_order_from_api(self, **kwargs):
		pass

	def fetch_order(self, **kwargs):
		try:
			order = fetch_order_from_db(kwargs['order_id'])
		except ValueError as e:
			logger.info(e)
			try:
				order = self.fetch_order_from_api(**kwargs)
				write_order_to_db(order)
				return order
			except ValueError as e:
				raise ValueError(e)
		return order

	def create_invoice(self, **kwargs):
		try:
			order = self.fetch_order(**kwargs)
		except Exception as e:
			raise ValueError(e)
		logger.info("Opening invoice template...")
		read_from = load_workbook(config_paths.input_excel_path + '/invoice.xlsx')
		read_sheet = read_from.active

		read_sheet['C8'].value = order.get_order_id()
		read_sheet['C8'].style = read_sheet['C8'].style
		read_sheet['C9'].value = order.invoice_no
		read_sheet['C10'].value = order.invoice_date
		read_sheet['C15'].value = order.buyer_name
		read_sheet['A16'].value = order.billing_addr_line1
		read_sheet['A17'].value = order.billing_addr_line2
		read_sheet['C19'].value = order.state
		read_sheet['G19'].value = order.state_code

		read_sheet['N8'].value = order.origin
		read_sheet['A37'].value = order.amount_in_words

		logger.info("Writing to new file...")
		row = 23
		for item in order.items:
			read_sheet['A' + str(row)].value = item.s_no
			read_sheet['B' + str(row)].value = item.desc_line1
			read_sheet['B' + str(row + 1)].value = item.desc_line2
			read_sheet['C' + str(row)].value = item.hsn_code
			read_sheet['D' + str(row)].value = item.qty
			read_sheet['E' + str(row)].value = item.rate
			read_sheet['G' + str(row)].value = item.discount
			read_sheet['I' + str(row)].value = item.cgst_rate
			read_sheet['K' + str(row)].value = item.sgst_rate
			read_sheet['M' + str(row)].value = item.igst_rate
			read_sheet['J' + str(row)].value = item.cgst_amt
			read_sheet['L' + str(row)].value = item.sgst_amt
			read_sheet['N' + str(row)].value = item.igst_amt
			row += 2

		op_path = config_paths.invoice_op_path + '/' + order.invoice_date
		if not does_dir_exist(op_path):
			create_dir(op_path + '/amazon')
			create_dir(op_path + '/flipkart')
			create_dir(op_path + '/other')

		read_from.save(op_path + "/" + order.origin + '/' + order.get_order_id() + '.xlsx')
		logger.info("Done!")

