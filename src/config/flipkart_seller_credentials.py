from src.util.common_functions import get_dir_path, read_property_file

parent_dir = get_dir_path()
creds = read_property_file(parent_dir + '/properties/flipkart_seller.credentials')

access_token = creds['access_token']
app_secret = creds['app_secret']
app_id = creds['app_id']
token_type = creds['token_type']
version = creds['version']
