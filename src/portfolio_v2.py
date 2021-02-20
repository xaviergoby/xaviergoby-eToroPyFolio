import os
import settings
import numpy as np
import pandas as pd
from src.stock_data import SingleStockTicker
from src import utils
import json


class AccStatementParser:
	
	def __init__(self, file_name):
		"""
		:param file_name: The file name of the eToro account statement xlsx, e.g. eToroAccountStatement.xlsx
		The purpose of this class is to parse the data stored in the account statement.
		"""
		self.file_name = file_name
		self.file_path = os.path.join(settings.ACC_STATEMENTS_DIR, self.file_name)
		self._all_crypto_symbols_list = utils.read_json_file("cryptocurrencies.json")
		self._acc_details_sheet_df = None
		self._closed_pos_sheet_df = None
		self._transactions_report_sheet_df = None
		self._fin_summary_sheet_df = None
		self._read_sheets_as_df()
	
	# self._read_acc_statement_sheets()
	# self._set_acc_details()
	
	def _read_acc_details_sheet_df(self):
		self._acc_details_sheet_df = pd.read_excel(self.file_path, sheet_name=0, engine='openpyxl')[['Details', 'Unnamed: 1']].reset_index().set_index(["Details"]).drop(["index"], axis=1)
	
	def _read_closed_pos_sheet_df(self):
		self._closed_pos_sheet_df = pd.read_excel(self.file_path, sheet_name=1, engine='openpyxl').drop(columns=["Copy Trader Name"])
	
	def _read_transactions_report_sheet_df(self):
		self._transactions_report_sheet_df = pd.read_excel(self.file_path, sheet_name=2, engine='openpyxl')
	
	def _read_fin_summary_sheet_df(self):
		self._fin_summary_sheet_df = pd.read_excel(self.file_path, sheet_name=3, engine='openpyxl')
	
	def _read_sheets_as_df(self):
		self._read_acc_details_sheet_df()
		self._read_closed_pos_sheet_df()
		self._read_transactions_report_sheet_df()
		self._read_fin_summary_sheet_df()
	
	@property
	def acc_details_sheet_df(self):
		if self._acc_details_sheet_df is None:
			self._read_acc_details_sheet_df()
		return self._acc_details_sheet_df
	
	@property
	def closed_pos_sheet_df(self):
		if self._closed_pos_sheet_df is None:
			self._read_closed_pos_sheet_df()
		return self._closed_pos_sheet_df
	
	@property
	def transactions_report_sheet_df(self):
		if self._transactions_report_sheet_df is None:
			self._read_transactions_report_sheet_df()
		return self._transactions_report_sheet_df
	
	@property
	def fin_summary_sheet_df(self):
		if self._fin_summary_sheet_df is None:
			self._read_fin_summary_sheet_df()
		return self._fin_summary_sheet_df
	
	### Account Details Sheet (#1) Processing
	
	def _gen_acc_details_dict(self):
		acc_details_sheet_dict = {}
		acc_details_sheet_dict["wd"] = float(pd.to_numeric(self.acc_details_sheet_df.loc["Withdrawals"]))
		acc_details_sheet_dict["wdf"] = float(pd.to_numeric(self.acc_details_sheet_df.loc["Withdrawal Fees"]))
		acc_details_sheet_dict["deposits"] = float(pd.to_numeric(self.acc_details_sheet_df.loc["Deposits"]))
		acc_details_sheet_dict["rof"] = float(pd.to_numeric(self.acc_details_sheet_df.loc["Rollover Fees"]))
		acc_details_sheet_dict["bre"] = float(pd.to_numeric(self.acc_details_sheet_df.loc["Beginning Realized Equity"]))
		acc_details_sheet_dict["bue"] = float(pd.to_numeric(self.acc_details_sheet_df.loc["Beginning Unrealized Equity"]))
		acc_details_sheet_dict["ere"] = float(pd.to_numeric(self.acc_details_sheet_df.loc["Ending Realized Equity"]))
		acc_details_sheet_dict["eue"] = float(pd.to_numeric(self.acc_details_sheet_df.loc["Ending Unrealized Equity"]))
		acc_details_sheet_dict["bue"] = float(pd.to_numeric(self.acc_details_sheet_df.loc["Beginning Unrealized Equity"]))
		acc_details_sheet_dict["eue"] = float(pd.to_numeric(self.acc_details_sheet_df.loc["Ending Unrealized Equity"]))
		acc_details_sheet_dict["tpl"] = float(pd.to_numeric(self.acc_details_sheet_df.loc["Trade Profit Or Loss (Closed positions only)"]))
		acc_details_sheet_dict["date_created"] = utils.standardize_dt_str_format(self.acc_details_sheet_df.loc["Date Created"][0])
		acc_details_sheet_dict["start_date"] = utils.standardize_dt_str_format(self.acc_details_sheet_df.loc["Start Date"][0])
		acc_details_sheet_dict["end_date"] = utils.standardize_dt_str_format(self.acc_details_sheet_df.loc["End Date"][0])
		return acc_details_sheet_dict
	
	@property
	def acc_details_dict(self):
		return self._gen_acc_details_dict()
	
	def _parse_order_fin_instrument_type(self, order_fin_instrument_name):
		"""
		:param closed_order_action_desc: e.g. "Buy Advanced Micro Devices Inc" or "Buy Bitcoin"
		:return:
		"""
		# order_fin_instrument_name = self._closed_pos_sheet_df["Action"][self._closed_pos_sheet_df["Position ID"] == closed_pos_id].values[0].lstrip("Buy").lstrip()
		# crypto_symbols_list = utils.read_json_file("cryptocurrencies.json")
		if order_fin_instrument_name.lstrip("Buy").lstrip() in list(self._all_crypto_symbols_list.values()):
			return "crypto"
		else:
			return "stock"
	
	### Closed Orders Sheet (#2) Processing
	def _closed_positions_df_reformatted(self):
		
		old_col_names = ["Position ID", "Action", "Leverage", "Amount", "Units", "Open Rate", "Close Rate", "Spread", "Profit",
		                 "Open Date", "Close Date", "Take Profit Rate", "Stop Loss Rate", "Rollover Fees And Dividends",
		                 "Is Real"]  # len 15
		new_col_names = ["Position ID", "Symbols", "Leverage", "Amount", "Units", "Open Rate", "Close Rate", "Spread", "Profit",
		                 "Open Date", "Close Date", "TP", "SL", "Rollover Fees&Dividends", "Type"]  # len 15
		closed_positions_col_data_dict = {}
		# for col_i_idx in range(len(old_col_names)):
		# 	old_col_name = old_col_names[col_i_idx]
		# 	new_col_name = new_col_names[col_i_idx]
		# 	closed_positions_col_data_dict[new_col_name] = self.closed_pos_sheet_df[old_col_name].iloc[:]
		
		closed_positions_col_data_dict["Position ID"] = self.closed_pos_sheet_df["Position ID"].iloc[:]
		closed_positions_col_data_dict["Symbols"] = self.closed_pos_sheet_df["Action"].iloc[:]
		closed_positions_col_data_dict["Name"] = self.closed_pos_sheet_df["Action"].apply(lambda action: action.split("Buy ")[-1])
		closed_positions_col_data_dict["Instrument Type"] = self.closed_pos_sheet_df["Action"].iloc[:].apply(lambda name: self._parse_order_fin_instrument_typev2(name))
		closed_positions_col_data_dict["Leverage"] = self.closed_pos_sheet_df["Leverage"].iloc[:]
		closed_positions_col_data_dict["Amount"] = self.closed_pos_sheet_df["Amount"].iloc[:]
		closed_positions_col_data_dict["Units"] = self.closed_pos_sheet_df["Units"].iloc[:]
		closed_positions_col_data_dict["Open Rate"] = self.closed_pos_sheet_df["Open Rate"].iloc[:]
		closed_positions_col_data_dict["Close Rate"] = self.closed_pos_sheet_df["Close Rate"].iloc[:]
		closed_positions_col_data_dict["Spread"] = self.closed_pos_sheet_df["Spread"].iloc[:]
		closed_positions_col_data_dict["Profit"] = self.closed_pos_sheet_df["Profit"].iloc[:]
		closed_positions_col_data_dict["Open Date"] = self.closed_pos_sheet_df["Open Date"].iloc[:]
		closed_positions_col_data_dict["Close Date"] = self.closed_pos_sheet_df["Close Date"].iloc[:]
		closed_positions_col_data_dict["TP"] = self.closed_pos_sheet_df["Take Profit Rate"].iloc[:]
		closed_positions_col_data_dict["SL"] = self.closed_pos_sheet_df["Stop Loss Rate"].iloc[:]
		closed_positions_col_data_dict["Rollover Fees&Dividends"] = self.closed_pos_sheet_df["Rollover Fees And Dividends"].iloc[:]
		closed_positions_col_data_dict["Type"] = self.closed_pos_sheet_df["Is Real"].iloc[:]
		
		new_closed_positions_df = pd.DataFrame(data=closed_positions_col_data_dict)
		new_closed_positions_df = new_closed_positions_df.reset_index().set_index(["Position ID"]).drop(["index"], axis=1)
		new_closed_positions_df["Open Date"] = new_closed_positions_df["Open Date"].apply(lambda dt_str: utils.standardize_dt_str_format(dt_str))
		new_closed_positions_df["Close Date"] = new_closed_positions_df["Close Date"].apply(lambda dt_str: utils.standardize_dt_str_format(dt_str))
		temp_closed_positions_df_copy = new_closed_positions_df.copy()
		transactions_report_sheet_df_copy = self.transactions_report_sheet_df.copy()
		closed_pos_symbols_list = []
		for closed_pos_i_idx in temp_closed_positions_df_copy.index:
			closed_pos_i_transactions_report = transactions_report_sheet_df_copy[transactions_report_sheet_df_copy["Position ID"] == float(closed_pos_i_idx)].copy()
			closed_pos_i_open_transaction_report = closed_pos_i_transactions_report[closed_pos_i_transactions_report["Type"] == "Profit/Loss of Trade"]
			closed_pos_i_symbol = closed_pos_i_open_transaction_report["Details"].values.copy()[0].split("/")[0]
			closed_pos_symbols_list.append(closed_pos_i_symbol)
		new_closed_positions_df["Symbols"] = closed_pos_symbols_list
		new_closed_positions_df_copy = new_closed_positions_df.copy()
		return new_closed_positions_df_copy
	
	@property
	def closed_orders_df(self):
		closed_orders_df_rebuilt = self._closed_positions_df_reformatted()
		return closed_orders_df_rebuilt
	
	### Open Orders Processing
	
	def _get_current_open_orders(self):
		common_pos_ids = self.transactions_report_sheet_df.merge(self.closed_pos_sheet_df, on=["Position ID"])
		remaining_pos_ids = self.transactions_report_sheet_df[~self.transactions_report_sheet_df["Position ID"].isin(common_pos_ids["Position ID"])]
		open_orders = remaining_pos_ids.loc[remaining_pos_ids["Position ID"].dropna().index][remaining_pos_ids["Type"] == "Open Position"].drop(columns=["Type"])
		open_orders_symbols = [open_order_symbol_currency_pair_i.rsplit("/")[0] for open_order_symbol_currency_pair_i in open_orders["Details"].values.tolist()]
		open_orders.insert(0, "Symbols", open_orders_symbols)
		self.open_orders_symbols = open_orders_symbols
		self._open_orders_df = open_orders
	
	def _get_current_open_orders_approx_avg_prices(self):
		open_orders_open_price = []
		open_orders_close_price = []
		open_orders_high_price = []
		open_orders_low_price = []
		open_orders_approx_avg_prices = []
		open_orders_dates = []
		open_orders_dates_times = []
		open_orders_units = []
		open_orders_returns = []
		open_orders_returns_pct = []
		for open_order_symbol_i in self.open_orders_symbols:
			open_order_yfinance_stock_data = SingleStockTicker(open_order_symbol_i).data
			open_order_symbol_i_buy_date_time = self._open_orders_df[self._open_orders_df["Symbols"] == open_order_symbol_i]["Date"].tolist()[0]
			open_orders_dates_times.append(open_order_symbol_i_buy_date_time)
			open_order_symbol_i_buy_date = open_order_symbol_i_buy_date_time.rsplit(" ")[0]
			open_orders_dates.append(open_order_symbol_i_buy_date)
			open_order_symbol_i_open_bar_data = open_order_yfinance_stock_data.loc[open_order_symbol_i_buy_date]
			open_orders_open_price.append(open_order_symbol_i_open_bar_data["open"])
			open_orders_close_price.append(open_order_symbol_i_open_bar_data["close"])
			open_orders_high_price.append(open_order_symbol_i_open_bar_data["high"])
			open_orders_low_price.append(open_order_symbol_i_open_bar_data["low"])
			
			open_order_symbol_i_avg_open_price = (open_order_symbol_i_open_bar_data["close"] + open_order_symbol_i_open_bar_data["open"]) / 2
			open_orders_approx_avg_prices.append(open_order_symbol_i_avg_open_price)
			open_order_symbol_i_amount_invested = self._open_orders_df[self._open_orders_df["Symbols"] == open_order_symbol_i]["Amount"].tolist()[0]
			open_order_symbol_i_units = np.round(open_order_symbol_i_amount_invested / open_order_symbol_i_avg_open_price, 2)
			open_orders_units.append(open_order_symbol_i_units)
			open_order_symbol_i_current_bar_data = open_order_yfinance_stock_data.loc[open_order_yfinance_stock_data.index.tolist()[-1]]
			open_order_symbol_i_most_recent_close_price = open_order_symbol_i_current_bar_data["close"]
			open_order_symbol_i_return = (open_order_symbol_i_most_recent_close_price - open_order_symbol_i_avg_open_price) * open_order_symbol_i_units
			open_orders_returns.append(open_order_symbol_i_return)
			open_order_symbol_i_return_pct = np.round(((open_order_symbol_i_most_recent_close_price / open_order_symbol_i_avg_open_price) - 1) * 100, 2)
			open_orders_returns_pct.append(open_order_symbol_i_return_pct)
		
		self._open_orders_df.insert(2, "Avg Open", open_orders_approx_avg_prices)
		self._open_orders_df.insert(3, "Open", open_orders_open_price)
		self._open_orders_df.insert(4, "High", open_orders_high_price)
		self._open_orders_df.insert(5, "Low", open_orders_low_price)
		self._open_orders_df.insert(6, "Close", open_orders_close_price)
		self._open_orders_df.insert(10, "Units", open_orders_units)
		self._open_orders_df.insert(11, "Returns", open_orders_returns)
		self._open_orders_df.insert(12, "Returns[%]", open_orders_returns_pct)
		self._open_orders_df["Date"] = self._open_orders_df["Date"].apply(lambda dt_str: utils.standardize_dt_str_format(dt_str))
		self._open_orders_df = self._open_orders_df.reset_index().set_index(["Position ID"]).drop(["index"], axis=1)
		self._open_orders_df["Details"] = self._open_orders_df["Details"].apply(lambda symbol_currency_pair: symbol_currency_pair.split("/")[1])
		self._open_orders_df = self._open_orders_df.rename(columns={"Date": "Open Date", "Details": "Currency"}, inplace=False)
	
	def _create_open_orders_df(self):
		self._get_current_open_orders()
		self._get_current_open_orders_approx_avg_prices()
	
	@property
	def open_orders_df(self):
		self._create_open_orders_df()
		return self._open_orders_df
	
	### Transactions Report Sheet (#3) Processing
	
	def _transactions_report_df_reformatted(self):
		transaction_dates = []
		pass
	
	### Financial Summary Sheet Processing //TODO
	
	### Ticker Symbols Processing //TODO
	def get_closed_pos_transaction_report(self):
		common_pos_ids = self.transactions_report_sheet_df.merge(self.closed_pos_sheet_df, on=["Position ID"])
		return common_pos_ids


# df = df[df.index.isin(df1.index)]
if __name__ == "__main__":
	pd.set_option('display.max_rows', 500)
	pd.set_option('display.max_columns', 500)
	pd.set_option('display.width', 500)
	# xlsx file date format: mm/dd/yyyy
	portfolio_xlsx_file_name = "eToroAccountStatement.xlsx"
	# portfolio_xlsx_file_name = "eToroAccountStatement - xaviergoby - 01-12-2020 - 01-12-2020"
	acc = AccStatementParser(portfolio_xlsx_file_name)
	closed_pos_transaction_report = acc.get_closed_pos_transaction_report()
	# print(f"closed_pos_transaction_report: {closed_pos_transaction_report}")
	closed_pos_open_transaction_report = closed_pos_transaction_report[closed_pos_transaction_report["Type"] == "Open Position"]
# print(f"closed_pos_open_transaction_report: {closed_pos_open_transaction_report}")

# print("Temp test code")
# transactions_report_sheet_df_copy = acc.transactions_report_sheet_df.copy()
# x = acc.transactions_report_sheet_df[acc.transactions_report_sheet_df["Type"] == "Profit/Loss of Trade"]
# symbols = x["Details"].apply(lambda symbol_currency_pair: symbol_currency_pair.split("/")[0])

# x["Details"] = x["Details"].apply(lambda symbol_currency_pair: symbol_currency_pair.split("/")[0])
# x.loc[:, "Details"] = x["Details"].apply(lambda symbol_currency_pair: symbol_currency_pair.split("/")[0])
# x.iloc[:, 3] = x["Details"].apply(lambda symbol_currency_pair: symbol_currency_pair.split("/")[0])

# x = acc.transactions_report_sheet_df[acc.transactions_report_sheet_df["Type"] == "Profit/Loss of Trade"]
# x_copy = x.copy()
# x_copy["Details"] = x_copy["Details"].apply(lambda symbol_currency_pair: symbol_currency_pair.split("/")[0])
# x_copy.loc[:, "Details"] = x_copy["Details"].apply(lambda symbol_currency_pair: symbol_currency_pair.split("/")[0])
# x_copy.iloc[:, 3] = x_copy["Details"].apply(lambda symbol_currency_pair: symbol_currency_pair.split("/")[0])


# res1 = acc.build_closed_positions_df()
