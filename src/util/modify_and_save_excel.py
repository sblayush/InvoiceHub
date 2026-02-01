from openpyxl import load_workbook
import src.config.config_paths as config_paths
from src.util.get_logger import MyLogger

logger = MyLogger.logger


def modify_and_save_excel(excel_name, order_obj):
	logger.info("Opening invoice template...")
	read_from = load_workbook(config_paths.input_excel_path + '/invoice1.xlsx')
	read_sheet = read_from.active

	read_sheet['C8'].value = order_obj["order_id"]
	read_sheet['C8'].style = read_sheet['C8'].style
	read_sheet['C9'].value = order_obj["invoice_no"]
	read_sheet['C10'].value = order_obj["invoice_date"]
	read_sheet['C15'].value = order_obj["buyer_name"]
	read_sheet['C16'].value = order_obj["billing_addr_line1"]
	read_sheet['C17'].value = order_obj["billing_addr_line2"]
	read_sheet['C19'].value = order_obj["state"]
	read_sheet['G19'].value = order_obj["state_code"]

	read_sheet['N8'].value = order_obj["origin"]
	read_sheet['A37'].value = order_obj["amount_in_words"]

	logger.info("Writing to new file...")
	row = 23
	for item in order_obj["items"]:
		read_sheet['A' + str(row)].value = item["s_no"]
		read_sheet['B' + str(row)].value = item["desc_line1"]
		read_sheet['B' + str(row+1)].value = item["desc_line2"]
		read_sheet['C' + str(row)].value = item["hsn_code"]
		read_sheet['D' + str(row)].value = item["qty"]
		read_sheet['E' + str(row)].value = item["rate"]
		read_sheet['G' + str(row)].value = item["discount"]
		read_sheet['I' + str(row)].value = item["cgst_rate"]
		read_sheet['K' + str(row)].value = item["sgst_rate"]
		read_sheet['M' + str(row)].value = item["igst_rate"]
		read_sheet['J' + str(row)].value = item["cgst_amt"]
		read_sheet['L' + str(row)].value = item["sgst_amt"]
		read_sheet['N' + str(row)].value = item["igst_amt"]
		row += 2

	filename = config_paths.invoice_op_path + '/07-Apr-2018/' + order_obj["origin"] + '/'
	read_from.save(filename + excel_name + '.xlsx')
	logger.info("Done!")

	import subprocess, sys

	opener = "libreoffice --headless --convert-to pdf " + filename  + excel_name + '.xlsx' + " " + filename
	subprocess.call(opener, shell=True)
