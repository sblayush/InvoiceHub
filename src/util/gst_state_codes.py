import json

json_dir = "/aboutPage.html/ayush/Desktop/pyCharm/MWS/python-amazon-mws/data/json"


def write_gst_codes():

	codes = """Andaman and Nicobar Islands:35:AN
	Andhra Pradesh:37:AD
	Arunachal Pradesh:12:AR
	Assam:18:AS
	Bihar:10:BR
	Chandigarh:04:CH
	Chattisgarh:22:CG
	Dadra and Nagar Haveli:26:DN
	Daman and Diu:25:DD
	Delhi:07:DL
	Goa:30:GA
	Gujarat:24:GJ
	Haryana:06:HR
	Himachal Pradesh:02:HP
	Jammu and Kashmir:01:JK
	Jharkhand:20:JH
	Karnataka:29:KA
	Kerala:32:KL
	Lakshadweep Islands:31:LD
	Madhya Pradesh:23:MP
	Maharashtra:27:MH
	Manipur:14:MN
	Meghalaya:17:ML
	Mizoram:15:MZ
	Nagaland:13:NL
	Odisha:21:OD
	Pondicherry:34:PY
	Punjab:03:PB
	Rajasthan:08:RJ
	Sikkim:11:SK
	Tamil Nadu:33:TN
	Telangana:36:TS
	Tripura:16:TR
	Uttar Pradesh:09:UP
	Uttarakhand:05:UK
	West Bengal:19:WB"""

	gst_codes_obj = {}

	for a in codes.split('\n'):
		split_arr = a.split(":")
		gst_codes_obj[split_arr[0].lower()] = {
				"tin": split_arr[1],
				"code": split_arr[2]
			}

	with open(json_dir+"/gst_state_codes.json", 'w') as f:
		json.dump(gst_codes_obj, f, indent=2)

	print("Codes written!")


def read_gst_codes():
	with open(json_dir+"/gst_state_codes.json", 'w') as f:
		gst_codes_obj = json.load(f)
