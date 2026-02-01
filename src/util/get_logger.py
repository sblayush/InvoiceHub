import logging.config
from datetime import datetime
import src.config.config_paths as config_paths
from src.util.common_functions import does_dir_exist, create_dir
from src.util.Singleton import Singleton

if not does_dir_exist(config_paths.log_op_path):
	create_dir(config_paths.log_op_path)
logFilePath = config_paths.log_op_path + '/log_' + datetime.now().strftime('%d_%m_%Y') + '.log'
logging.config.fileConfig(config_paths.log_config_path, defaults={'logfilename': logFilePath})


class MyLogger(Singleton):
	logger = logging.getLogger("log1")

	@staticmethod
	def get_logger():
		return MyLogger.logger

