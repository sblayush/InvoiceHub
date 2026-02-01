from src.util.common_functions import get_dir_path, read_property_file

creds = read_property_file(get_dir_path() + '/properties/seller.credentials')

gstin_no = creds['gstin']
invoice_text = creds['invoice_text']
