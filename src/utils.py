import settings
import os
import json
import pandas as pd
import datetime
import dateutil
from dateutil.parser import parse
from fuzzywuzzy import process
import requests


def getCompany(text):
	r = requests.get('https://api.iextrading.com/1.0/ref-data/symbols')
	stockList = r.json()
	return process.extract(text, stockList)
	# return process.extractOne(text, stockList)
	# return process.extractOne(text, stockList)[0]

def convert_dt_str_2_dt_obj(dt_str):
	"""
	Recall that the standard representation/format of datetime strings used in this system is: "%d/%m/%Y %H:%M"
	acc_details_US_dt_format="%-m/%-d/%Y %-I:%M:%S %p"  e.g. 12/20/2020 7:02:01 PM
	closed_pos_EU_dt_format="%d/%m/%Y %H:%M"    e.g. 16/06/2020 13:30
	transaction_report_JAP_dt_format="%Y-%m-%d %H:%M:%S"    e.g. 2020-06-16 13:30:05
	:param dt_str: A string of the U.S., E.U. or Japanese date time format str to standardize.
	:return: A datetime.datetime of the resulting standardisation (EU dt str format based) of dt_str
	"""
	if "PM" in dt_str or "AM" in dt_str:
		# So therefore dt_str has the US format of: "%-m/%-d/%Y %-I:%M:%S %p"
		dt_obj = parse(parse(dt_str).__str__()[:-3])
	elif "-" in dt_str:
		# So therefore dt_str has the JAP format of: "%Y-%m-%d %H:%M:%S"
		dt_obj = parse(datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S").__str__()[:-3])
	else:
		# Only the EU dt format left therefore its obv that dt_str has the EU dt format of: "%d/%m/%Y %H:%M"
		dt_obj = datetime.datetime.strptime(dt_str, "%d/%m/%Y %H:%M")
	return dt_obj

def standardize_dt_str_format(dt_str):
	"""
	:param dt_str: A string of the U.S., E.U. or Japanese date time format str to standardize.
	:return: An str of the resulting standardisation (EU dt str format based) of dt_str
	"""
	dt_obj = convert_dt_str_2_dt_obj(dt_str)
	dt_str = dt_obj.strftime("%d/%m/%Y %H:%M")
	return dt_str

def extract_dt_date(dt_str, date_format="%Y-%m-%d"):
	"""
	:param dt_str: a str of the datetime having either a U.S., E.U. or Jap datetime format
	:param date_format: The str format of the date to transform the extracted date into. Uses
	the E.U. date formatting, "%Y-%m-%d", by default.
	:return: str of only the date in E.U., "%Y-%m-%d", format if date_format is unchanged else formatted
	as date_format
	"""
	dt_obj = convert_dt_str_2_dt_obj(dt_str)
	dt_date_str = dt_obj.strftime(date_format)
	return dt_date_str

def read_json_file(file_name):
	file_path = os.path.join(settings.FIN_INSTRUMENTS_DIR, file_name)
	with open(file_path) as json_file:
		data = json.load(json_file)
	return data
	
# def _build_datetime_range_index(start_date, end_date):
#
# 	start_date = self.acc_details.start_date.split(" ")[0]
# 	end_date = self.acc_details.end_date.split(" ")[0]
# 	dt_index = pd.date_range(start=start_date, end=end_date)
# 	return dt_index
#

if __name__ == "__main__":
	t1 = "12/20/2020 7:02:01 PM" # U.S.
	t2 = "2020-06-16 13:30:05" # JAP
	t3 = "06/07/2020 16:25" # E.U.
	
	std_t1_obj = convert_dt_str_2_dt_obj(t1)
	std_t2_obj = convert_dt_str_2_dt_obj(t2)
	std_t3_obj = convert_dt_str_2_dt_obj(t3)
	
	print(repr(std_t1_obj))
	print(repr(std_t2_obj))
	print(repr(std_t3_obj))
	
	std_t1 = standardize_dt_str_format(t1)
	std_t2 = standardize_dt_str_format(t2)
	std_t3 = standardize_dt_str_format(t3)
	
	print(std_t1)
	print(std_t2)
	print(std_t3)
	
	# getCompany('GOOG')
	# getCompany('Alphabet')
	getCompany("DocuSign Inc")
	getCompany("Advanced Micro Devices Inc")
	getCompany("Tesla Motors")
	
	cryptos_list = read_json_file("cryptocurrencies.json")
	
