import os
import settings
import numpy as np
import pandas as pd
from src.stock_data import SingleStockTicker


class AccStatementParser:
	
	def __init__(self, portfolio_xlsx_file_name):
		self.portfolio_xlsx_file_name = portfolio_xlsx_file_name
		self.xlsx_file_path = os.path.join(settings.DATA_DIR, self.portfolio_xlsx_file_name)
		
		self.acc_details = pd.read_excel(self.xlsx_file_path, sheet_name=0, engine='openpyxl')[['Details', 'Unnamed: 1']].reset_index().set_index(["Details"]).drop(["index"], axis=1)  # //TODO Discard
		self._closed_positions = pd.read_excel(self.xlsx_file_path, sheet_name=1, engine='openpyxl')  # //TODO Discard
		self.transactions_report = pd.read_excel(self.xlsx_file_path, sheet_name=2, engine='openpyxl')  # //TODO Discard
		self.fin_summary = pd.read_excel(self.xlsx_file_path, sheet_name=3, engine='openpyxl')  # //TODO Discard
		
		self.withdrawals = float(pd.to_numeric(self.acc_details.loc["Withdrawals"])) #//TODO Discard
		self.withdrawal_fees = float(pd.to_numeric(self.acc_details.loc["Withdrawal Fees"])) #//TODO Discard
		self.init_beginning_realized_equity = float(pd.to_numeric(self.acc_details.loc["Beginning Realized Equity"]))  # //TODO Discard
		self.deposits = float(pd.to_numeric(self.acc_details.loc["Deposits"]))  # //TODO Discard
		self.tot_roll_over_fees = float(pd.to_numeric(self.acc_details.loc["Rollover Fees"]))  # //TODO Discard
		self.current_realized_profit = float(pd.to_numeric(self.acc_details.loc["Trade Profit Or Loss (Closed positions only)"]))  # //TODO Discard
		self.init_ending_unrealized_equity = float(pd.to_numeric(self.acc_details.loc["Ending Unrealized Equity"]))  # //TODO Discard
		
		self.tot_withdrawal_amount = float(pd.to_numeric(self.acc_details.loc["Withdrawals"]) + pd.to_numeric(self.acc_details.loc["Withdrawal Fees"]))
		self.init_ending_realized_equity = float(pd.to_numeric(self.acc_details.loc["Ending Realized Equity"]))
		self.current_unrealized_profit = self.init_ending_unrealized_equity - self.init_ending_realized_equity
		self.total_profit = self.current_realized_profit + self.current_unrealized_profit
		self._get_current_open_orders()
		self._set_additional_derived_values()
		self._get_current_open_orders_approx_avg_prices()
		self._clean_open_orders_df()
		self._set_closed_orders()
		self._set_acc_details()
		
	def _read_acc_statement_sheets(self):
		self.acc_details = pd.read_excel(self.xlsx_file_path, sheet_name=0, engine='openpyxl')[['Details', 'Unnamed: 1']].reset_index().set_index(["Details"]).drop(["index"], axis=1)
		self._closed_positions = pd.read_excel(self.xlsx_file_path, sheet_name=1, engine='openpyxl')
		self.transactions_report = pd.read_excel(self.xlsx_file_path, sheet_name=2, engine='openpyxl')
		self.fin_summary = pd.read_excel(self.xlsx_file_path, sheet_name=3, engine='openpyxl')
		
	def _acc_details_sheet_dict(self):
		acc_details_sheet_dict = {}
		acc_details_sheet_dict["wd"] = float(pd.to_numeric(self.acc_details.loc["Withdrawals"]))
		acc_details_sheet_dict["wdf"] = float(pd.to_numeric(self.acc_details.loc["Withdrawal Fees"]))
		acc_details_sheet_dict["deposits"] = float(pd.to_numeric(self.acc_details.loc["Deposits"]))
		acc_details_sheet_dict["rof"] = float(pd.to_numeric(self.acc_details.loc["Rollover Fees"]))
		acc_details_sheet_dict["bre"] = float(pd.to_numeric(self.acc_details.loc["Beginning Realized Equity"]))
		acc_details_sheet_dict["ere"] = float(pd.to_numeric(self.acc_details.loc["Ending Unrealized Equity"]))
		acc_details_sheet_dict["tpl"] = float(pd.to_numeric(self.acc_details.loc["Trade Profit Or Loss (Closed positions only)"]))
		acc_details_sheet_dict["date_created"] = pd.to_datetime(self.acc_details.loc["Date Created"][0], format="%m/%d/%Y %H:%M:%S %p")
		acc_details_sheet_dict["start_date"] = pd.to_datetime(self.acc_details.loc["Start Date"][0], format="%m/%d/%Y %H:%M:%S %p")
		acc_details_sheet_dict["end_date"] = pd.to_datetime(self.acc_details.loc["End Date"][0], format="%m/%d/%Y %H:%M:%S %p")
		return acc_details_sheet_dict
	
	def _set_acc_details(self):
		acc_details_dict = self._acc_details_sheet_dict()
		for key, val in acc_details_dict.items():
			self.__dict__[key] = val
			
	def set_acc_details(self):
		self._set_acc_details()
		
	
	def __str__(self):
		info = f"Beginning Realized Equity: {self.init_beginning_realized_equity}[$]\n" \
		       f"Deposits: {self.deposits}[$]\n" \
		       f"Trade Profit Or Loss (Closed positions only): {self.current_realized_profit}[$]\n" \
		       f"Withdrawals: {self.withdrawals}[$]\n" \
		       f"Withdrawal Fees: {self.withdrawal_fees}[$]\n" \
		       f"Total of Withdrawals: {self.tot_withdrawal_amount}[$]\n" \
		       f"Rollover Fees: {self.tot_roll_over_fees}[$]\n" \
		       f"Ending Realized Equity (Total Allocated+Available): {self.init_ending_realized_equity}[$]\n" \
		       f"Ending Unrealized Equity ('Equity'): {self.init_ending_unrealized_equity}[$]\n" \
		       f"{'#' * 75}\n" \
		       f"Total Profit (=Trade Profit Or Loss + Current Unrealized Profit): {self.total_profit}[$]\n" \
		       f"Current Unrealized Profit ('Profit'): {self.current_unrealized_profit}[$]\n" \
		       f"Current Amount Invested ('Total Allocated'): {self.total_allocated}[$]\n" \
		       f"Current Balance Available ('Available'): {self.available}[$]\n"
		return info
	
	def _get_current_open_orders(self):
		common_pos_ids = self.transactions_report.merge(self._closed_positions, on=["Position ID"])
		remaining_pos_ids = self.transactions_report[~self.transactions_report["Position ID"].isin(common_pos_ids["Position ID"])]
		open_orders = remaining_pos_ids.loc[remaining_pos_ids["Position ID"].dropna().index][remaining_pos_ids["Type"] == "Open Position"].drop(columns=["Type"])
		# self.open_orders = open_orders.drop(columns=["Type"])
		open_orders_symbols = [open_order_symbol_currency_pair_i.rsplit("/")[0] for open_order_symbol_currency_pair_i in open_orders["Details"].values.tolist()]
		# open_orders["Details"] = open_orders_symbols
		open_orders.insert(0, "Symbols", open_orders_symbols)
		self.open_orders_symbols = open_orders_symbols
		self.open_orders = open_orders
	
	# open_orders.insert(2, "Symbols", [21, 23, 24, 21], True)
	
	def _set_additional_derived_values(self):
		self.total_allocated = self.open_orders["Amount"].sum()
		self.available = np.round(self.init_ending_unrealized_equity - (self.total_allocated + self.current_unrealized_profit), 2)
	
	# self.equity = self.total_allocated + self.current_unrealized_profit
	
	# def _get_current_open_orders_symbols(self):
	# 	self.open_orders_symbols = [open_order_symbol_currency_pair_i.rsplit("/")[0] for open_order_symbol_currency_pair_i in self.open_orders["Details"].values.tolist()]
	
	def _get_current_open_orders_approx_avg_prices(self):
		# docu_open_order_buy_date_val = docu_open_order_buy_date.values.tolist()[0].rsplit(" ")[0]
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
			# open_order_symbol_i_buy_date_time = self.open_orders[self.open_orders["Details"] == open_order_symbol_i]["Date"].tolist()[0]
			open_order_symbol_i_buy_date_time = self.open_orders[self.open_orders["Symbols"] == open_order_symbol_i]["Date"].tolist()[0]
			open_orders_dates_times.append(open_order_symbol_i_buy_date_time)
			open_order_symbol_i_buy_date = open_order_symbol_i_buy_date_time.rsplit(" ")[0]
			open_orders_dates.append(open_order_symbol_i_buy_date)
			open_order_symbol_i_open_bar_data = open_order_yfinance_stock_data.loc[open_order_symbol_i_buy_date]
			open_orders_open_price.append(open_order_symbol_i_open_bar_data["Open"])
			open_orders_close_price.append(open_order_symbol_i_open_bar_data["Close"])
			open_orders_high_price.append(open_order_symbol_i_open_bar_data["High"])
			open_orders_low_price.append(open_order_symbol_i_open_bar_data["Low"])
			
			open_order_symbol_i_avg_open_price = (open_order_symbol_i_open_bar_data["Close"] + open_order_symbol_i_open_bar_data["Open"]) / 2
			open_orders_approx_avg_prices.append(open_order_symbol_i_avg_open_price)
			open_order_symbol_i_amount_invested = self.open_orders[self.open_orders["Symbols"] == open_order_symbol_i]["Amount"].tolist()[0]
			open_order_symbol_i_units = np.round(open_order_symbol_i_amount_invested / open_order_symbol_i_avg_open_price, 2)
			open_orders_units.append(open_order_symbol_i_units)
			open_order_symbol_i_current_bar_data = open_order_yfinance_stock_data.loc[open_order_yfinance_stock_data.index.tolist()[-1]]
			open_order_symbol_i_most_recent_close_price = open_order_symbol_i_current_bar_data["Close"]
			open_order_symbol_i_return = (open_order_symbol_i_most_recent_close_price - open_order_symbol_i_avg_open_price) * open_order_symbol_i_units
			open_orders_returns.append(open_order_symbol_i_return)
			open_order_symbol_i_return_pct = np.round(((open_order_symbol_i_most_recent_close_price / open_order_symbol_i_avg_open_price) - 1) * 100, 2)
			open_orders_returns_pct.append(open_order_symbol_i_return_pct)
		# open_orders_approx_avg_prices.append((open_order_symbol_i_open_bar_data["Close"] + open_order_symbol_i_open_bar_data["Open"]) / 2)
		# self.open_orders_approx_avg_prices = open_orders_approx_avg_prices
		self.open_orders.insert(2, "Avg Open", open_orders_approx_avg_prices)
		self.open_orders.insert(3, "Open", open_orders_open_price)
		self.open_orders.insert(4, "High", open_orders_high_price)
		self.open_orders.insert(5, "Low", open_orders_low_price)
		self.open_orders.insert(6, "Close", open_orders_close_price)
		self.open_orders.insert(10, "Units", open_orders_units)
		self.open_orders.insert(11, "Returns", open_orders_returns)
		self.open_orders.insert(12, "Returns[%]", open_orders_returns_pct)
	
	def _clean_open_orders_df(self):
		self.open_orders = self.open_orders.drop(columns=["Account Balance", "Realized Equity Change"])
	
	def _build_closed_orders_df(self):
		pass
		# self.closed_positions
	
	# self.open_orders["Date"] = [open_order_i_buy_date.rsplit(" ")[0] for open_order_i_buy_date in self.open_orders["Date"].values.tolist()]
	
	def _build_closed_positions_df(self):
		old_col_names = ["Position ID", "Action", "Amount", "Units", "Open Rate", "Close Rate", "Spread", "Profit",
		                 "Open Date", "Close Date", "Take Profit Rate", "Stop Loss Rate", "Rollover Fees And Dividends",
		                 "Is Real",
		                 "Leverage"]
		new_col_names = ["ID", "Side", "Amount", "Units", "Open Rate", "Close Rate", "Spread", "Profit",
		                 "Open Date", "Close Date", "TP", "SL", "Fees&Dividends", "Type", "Leverage"]
		closed_positions_col_data_dict = {}
		for col_i_idx in range(len(old_col_names)):
			old_col_name = old_col_names[col_i_idx]
			new_col_name = new_col_names[col_i_idx]
			closed_positions_col_data_dict[new_col_name] = self._closed_positions[old_col_name].iloc[:]
		new_closed_positions_df = pd.DataFrame(data=closed_positions_col_data_dict)
		new_closed_positions_df["Open Date"] = pd.to_datetime(new_closed_positions_df["Open Date"]).dt.strftime(
				"%d/%m/%Y")
		new_closed_positions_df["Close Date"] = pd.to_datetime(new_closed_positions_df["Close Date"]).dt.strftime(
				"%d/%m/%Y")
		new_closed_positions_df = new_closed_positions_df.reset_index().set_index(["ID"]).drop(["index"], axis=1)
		return new_closed_positions_df
	
	def _set_closed_orders(self):
		closed_orders = self._closed_positions.drop(columns=["Copy Trader Name"])
		self.closed_orders = closed_orders
	
	# def _build_transactions_report_df(self):
	# 	old_col_names = ["Date", "Account Balance", "Type", "Details", "Position ID", "Amount", "Realized Equity Change", "Realized Equity"]
	# 	# old_col_names = ["Date", "Account Balance", "Type", "Details", "Position ID", "Amount", "Realized Equity Change", "Realized Equity"]
	# 	#
	# 	# old_col_names = ["Position ID", "Details", "Type", "Account Balance", "Position ID", "Amount", "Realized Equity Change", "Realized Equity"]
	# 	#
	# 	# new_col_names = ["ID", "Details", "Type", "Size", ""]
	#
	# 	new_transactions_report_df = self.transactions_report[old_col_names].reset_index().set_index(["Position ID"]).drop(["index"], axis=1)
	# 	new_transactions_report_df = new_transactions_report_df[new_transactions_report_df["Type"] == "Profit/Loss of Trade"]
	# 	return new_transactions_report_df
	#
	# def build_transactions_report_df(self):
	# 	return self._build_transactions_report_df()
	
	# def _reformat_close_transactions_df(self):
	# 	unformated_built_close_transactions_df = self.build_transactions_report_df()
	# 	unformated_side_col_vals = unformated_built_close_transactions_df["Side"].values


# df = df[df.index.isin(df1.index)]
if __name__ == "__main__":
	# pd.set_option('display.max_rows', 500)
	pd.set_option('display.max_columns', 500)
	pd.set_option('display.width', 500)
	# xlsx file date format: mm/dd/yyyy
	portfolio_xlsx_file_name = "eToroAccountStatement.xlsx"
	# portfolio_xlsx_file_name = "eToroAccountStatement - xaviergoby - 01-12-2020 - 01-12-2020"
	acc = AccStatementParser(portfolio_xlsx_file_name)
	print(acc)
	# res1 = acc.build_closed_positions_df()
	print(acc.open_orders)
	print(type(acc.acc_details))
	print(type(acc.transactions_report))
	print(type(acc._closed_positions))
	print(type(acc.fin_summary))
	
	date_created = acc.date_created
	start_date = acc.start_date
	end_date = acc.end_date
	
	bre = acc.bre
	
	print(date_created.date())
	print(start_date.date())
	print(end_date.date())
	
	acc_dt_range = pd.date_range(start=start_date.date(), end=end_date.date())
	print(f"acc_dt_range: {acc_dt_range}")
	acc_transactions_report_df_copy = acc.transactions_report.copy()
	acc_transactions_report_dt_idx = pd.to_datetime(acc_transactions_report_df_copy["Date"], format='%Y-%m-%d')
	print(acc_transactions_report_dt_idx)
	transactions_report_copy = acc_transactions_report_df_copy.copy()
	transactions_report_copy["Date"] = acc_transactions_report_dt_idx
	print(type(transactions_report_copy))
	type(transactions_report_copy)
	print(type(transactions_report_copy["Date"]))
	type(transactions_report_copy["Date"])

# res2 = acc.build_transactions_report_df()
# common_pos_ids = acc.transactions_report.merge(acc.closed_positions, on=["Position ID"])
# remaining_pos_ids = acc.transactions_report[~acc.transactions_report["Position ID"].isin(common_pos_ids["Position ID"])]


# resultv2 = acc.transactions_report.merge(acc.closed_positions, on=["Position ID"])[~acc.transactions_report["Position ID"].isin(common["Position ID"])]
# open_orders = acc.transactions_report[~acc.transactions_report["Position ID"].isin(common["Position ID"])].loc[result["Position ID"].dropna().index]
# print(result)
# print(res2)
# res3 = res2[res2.index.isin(res1.index)]
# print(acc.closed_positions)
# print(res)
# print(type(res["Open Date"].iloc[0]))
# xlsx_file_path = r"C:\Users\Xavier\AI-Algorithmic-Trading-System\data\eToroAccountStatement.xlsx"
# acc_details = pd.read_excel(xlsx_file_path, sheet_name=0)[['Details', 'Unnamed: 1']].loc[:22]
# closed_positions = pd.read_excel(xlsx_file_path, sheet_name=1)
# transactions_report = pd.read_excel(xlsx_file_path, sheet_name=2)
# fin_summary = pd.read_excel(xlsx_file_path, sheet_name=3)
# acc_info = pd.read_excel(xlsx_file_path)
# print(f"acc_info.columns: {acc_info.columns}")
# print(f"acc_info['Unnamed: 1']: {acc_info['Unnamed: 1']}")
# print(f"acc_info['Details']: {acc_info['Details']}")
# print(f"acc_info[['Details', 'Unnamed: 1']]: {acc_info[['Details', 'Unnamed: 1']]}")
# acc_details = acc_info[['Details', 'Unnamed: 1']].loc[:22]
# print(f"acc_info[['Details', 'Unnamed: 1']].loc[:22]: {acc_info[['Details', 'Unnamed: 1']].loc[:22]}")
# print(f"eToro Account Information: {acc_details}")
# tot_withdrawal_sum = sum(pd.to_numeric(acc_details["Unnamed: 1"].loc[16:17]))
# print(f"Total Amount of Fund Withdrawals: {tot_withdrawal_sum}")
# [open_order_symbol_currency_pair_i.rsplit("/")[0] for open_order_symbol_currency_pair_i in acc.open_orders["Details"].values.tolist()]
