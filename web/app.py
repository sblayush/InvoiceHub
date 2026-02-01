import json
import src.config.config_paths as config_paths
from src.util.common_functions import does_dir_exist, create_dir, get_os_type
from src.actions.FlipkartVendor import FlipkartVendor
from src.actions.AmazonVendor import AmazonVendor
from src.actions.OtherVendor import OtherVendor
from src.actions.EditInvoice import EditInvoice
from src.actions.GetOrdersForMonth import get_orders_for_month
from flask import Flask, render_template, request, Response
from src.util.get_logger import MyLogger

logger = MyLogger.logger

avc = AmazonVendor()
fvc = FlipkartVendor()
ovc = OtherVendor()
eic = EditInvoice()
app = Flask(__name__)
if get_os_type() == 'Windows':
	from src.util import apply_excel_patch


@app.route("/")
def main():
	return render_template('index.html')


@app.route("/createInvoice", methods=['POST'])
def create_invoice():
	req = json.loads(request.data.decode("utf-8"))
	logger.info("Got request:")
	logger.info(req)

	origin = req["origin"]
	if origin == "amazon":
		hsn = req["hsn"]
		try:
			avc.create_invoice(order_id=req["order_id"], hsn=hsn)
		except Exception as e:
			logger.exception(str(e))
			return Response("Failure", status=100)
	elif origin == "flipkart":
		try:
			fvc.create_invoice(order_id=req["order_id"])
		except Exception as e:
			logger.exception(str(e))
			return Response("Failure", status=100)
	else:
		try:
			ovc.create_invoice(**req["order"])
		except Exception as e:
			logger.exception(str(e))
			return Response("Failure", status=100)
	return "Success"


@app.route("/editInvoice", methods=['POST'])
def edit_invoice():
	req = json.loads(request.data.decode("utf-8"))
	logger.info("Got request:")
	logger.info(req)

	order_id = req['order_id']
	try:
		order = eic.get_invoice_from_db(order_id)
		logger.info(order)
		return Response(json.dumps(order), status=200, mimetype="application/json")
	except Exception as e:
		logger.exception(str(e))
		return Response("Failure", status=100)


@app.route("/getOrdersForMonth", methods=["POST"])
def get_month_orders():
	req = json.loads(request.data.decode("utf-8"))
	logger.info("Got request:")
	logger.info(req)

	try:
		orders_list = get_orders_for_month(**req)
		return Response(json.dumps(orders_list), status=200, mimetype="application/json")
	except Exception as e:
		logger.exception(e)
		return Response("Failure",  status=100)


def start_app():
	app.logger.disabled = True
	app.run(port=config_paths.port_no)


if __name__ == "__main__":
	if not does_dir_exist(config_paths.log_op_path):
		create_dir(config_paths.log_op_path)
	start_app()
