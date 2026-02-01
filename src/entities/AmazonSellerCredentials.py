from src.util.common_functions import get_dir_path, read_property_file
from src.util.Singleton import Singleton

parent_dir = get_dir_path()
creds = read_property_file(parent_dir + '/properties/amazon_seller.credentials')


class AmazonSellerCredentials(metaclass=Singleton):
	access_key = creds['access_key']
	secret_key = creds['secret_key']
	account_id = creds['account_id']
	region = creds['region']
	domain = creds['domain']
	uri = creds['uri']
	version = creds['version']
	auth_token = creds['auth_token']
