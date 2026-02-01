import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)).replace('\\', '/'))
sys.path.append(parent_dir)
from web.app import start_app
from src.util.get_logger import MyLogger

logger = MyLogger.logger


if __name__ == '__main__':
	start_app()
