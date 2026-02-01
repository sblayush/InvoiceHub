import num2words
import re
import os
import platform


def get_dir_path():
	return os.path.dirname(os.path.dirname((os.path.dirname(os.path.realpath(__file__))))).replace('\\', '/')


def does_dir_exist(path):
	return os.path.exists(path)


def create_dir(path):
	if not os.path.exists(path):
		os.makedirs(path)


def read_property_file(file_path):
	const_obj = {}
	with open(file_path, 'r') as f:
		for line in f.readlines():
			key, val = line.strip().split('=')
			const_obj[key] = val
	return const_obj


def get_tax_rates(total_rate, my_state, coming_state):
	total_rate = float(total_rate)
	cgst, sgst, igst = 0, 0, 0
	if my_state == coming_state:
		cgst, sgst = total_rate/2, total_rate/2
	else:
		igst = total_rate
	return cgst, sgst, igst


def get_tax_amt(total_amt, my_state, coming_state):
	cgst, sgst, igst = 0, 0, 0
	my_state = ['uttar pradesh', 'uttarpradesh', 'up', 'u p', 'u.p', 'u.p.', 'uttr pradesh']
	if coming_state in my_state:
		cgst, sgst = total_amt/2, total_amt/2
	else:
		igst = total_amt
	return cgst, sgst, igst


def convert_num_to_words(num):
	return (num2words.num2words(num, to='cardinal', lang='en_IN') + " only").title()


def get_net_size(sku_id):
	size_arr = re.findall('\d+', sku_id)
	if len(size_arr) == 2:
		siz = size_arr[0] + "ft x" + size_arr[1] + "ft"
	else:
		siz = size_arr[0] + "ft x " + size_arr[1] + "." + size_arr[2] + "ft"
	return siz


def get_os_type():
	return platform.system()


def get_invoice_name(_id):
	creds = read_property_file(get_dir_path() + '/properties/seller.credentials')
	invoice_text = creds['invoice_text']
	if _id < 10:
		invoice_name = invoice_text + '000' + str(_id)
	elif 9 < _id < 100:
		invoice_name = invoice_text + '00' + str(_id)
	elif 99 < _id < 999:
		invoice_name = invoice_text + '0' + str(_id)
	else:
		invoice_name = invoice_text + str(_id)
	return invoice_name


if __name__ == '__main__':
	print(get_os_type())
