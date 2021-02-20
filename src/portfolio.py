from src.xlsx_file_parser_improved import AccStatementParser
from src.acc_details import AccountDetails
from src.closed_orders import ClosedOrders
from src.transactions_report import TransactionsReport
from src.open_orders import OpenOrders
from src.order_book import OrderBook
import plotly.graph_objects as go
from src import utils
import pandas as pd
import matplotlib.pyplot as plt


class Portfolio:
	
	def __init__(self, acc_statement):
		self.acc_statement = acc_statement
		self.acc_statement_parser = AccStatementParser(acc_statement)
		# self._acc_details = AccountDetails(self.acc_statement_parser.acc_details_dict)
		self.acc_details = AccountDetails(self.acc_statement_parser.acc_details_dict)
		self.init_equity = self.acc_details.bre
		self.closed_orders = ClosedOrders(self.acc_statement_parser.closed_orders_df)
		self.instruments_prev_traded = self.closed_orders.closed_orders_df["Symbols"].unique().tolist()
		self.transactions_report = TransactionsReport(self.acc_statement_parser.transactions_report_sheet_df) # //TODO
		self.open_orders = OpenOrders(self.acc_statement_parser.open_orders_df)
		self.order_book = OrderBook()
		self.instruments_currently_trading = self.open_orders.open_orders_df["Symbols"].unique().tolist()
		self._build_daily_total_realized_equity()
		
	def _build_datetime_index(self):
		start_date = self.acc_details.start_date.split(" ")[0]
		end_date = self.acc_details.end_date.split(" ")[0]
		dt_index = pd.date_range(start=start_date, end=end_date)
		return dt_index
	
	def _build_daily_portfolio_equity_placeholder(self):
		daily_equity_placeholder_df = pd.DataFrame(columns=["Daily Portfolio Equity"], index=self._build_datetime_index())
		# daily_equity_placeholder_df = daily_equity_placeholder_df.fillna(0)
		return daily_equity_placeholder_df
	
	def _extract_transactions_report_realized_equity_df(self):
		transactions_report_sheet_df_copy = self.acc_statement_parser.transactions_report_sheet_df.copy()
		transactions_report_dts_list = transactions_report_sheet_df_copy["Date"].apply(lambda dt_str: dt_str.split(" ")[0]).to_list()
		transactions_report_realized_equity_list = transactions_report_sheet_df_copy["Realized Equity"].to_list()
		transactions_report_realized_equity_df = pd.DataFrame({"Realized Equity": transactions_report_realized_equity_list}, index=transactions_report_dts_list)
		transactions_report_realized_equity_unique_dt_idxs_list = transactions_report_realized_equity_df.index.unique()
		end_of_day_realized_equity_list = []
		# current_row_dt_idx = transactions_report_realized_equity_df.index[0]
		for unique_dt_idx in transactions_report_realized_equity_unique_dt_idxs_list:
			# print(f"unique_dt_idx: {unique_dt_idx}")
			end_of_day_realized_equity_list.append(float(transactions_report_realized_equity_df.loc[unique_dt_idx].values[-1]))
		# return transactions_report_realized_equity_df
		transactions_report_daily_end_of_day_realized_equity_df = pd.DataFrame({"Realized Equity": end_of_day_realized_equity_list}, index=pd.DatetimeIndex(transactions_report_realized_equity_unique_dt_idxs_list))
		# transactions_report_daily_end_of_day_realized_equity_df.index = pd.to_datetime(transactions_report_daily_end_of_day_realized_equity_df.index)
		return transactions_report_daily_end_of_day_realized_equity_df
	
	def _build_daily_realized_equity_df(self):
		daily_equity_placeholder_df = self._build_daily_portfolio_equity_placeholder()
		transactions_report_realized_equity_df = self._extract_transactions_report_realized_equity_df()
		daily_equity_df = pd.concat([daily_equity_placeholder_df, transactions_report_realized_equity_df], axis=1)
		# daily_equity_df = daily_equity_df.fillna(0)
		# closed_pos_daily_rets = self.closed_orders.closed_pos_daily_rets
		# daily_equity_df = pd.concat([daily_equity_df, closed_pos_daily_rets])
		# daily_equity_df = daily_equity_df.fillna(0)
		return daily_equity_df
	
	def _build_daily_total_realized_equity(self):
		daily_realized_equity_df = self._build_daily_realized_equity_df()
		# closed_pos_daily_rets = self.closed_orders.closed_pos_daily_rets
		# closed_pos_daily_rets = self.closed_orders.pos_daily_returns_df.sum(axis=1)
		open_pos_daily_rets = self.open_orders.open_pos_daily_rets
		daily_equity_df = pd.concat([daily_realized_equity_df, open_pos_daily_rets], axis=1)
		daily_equity_df["Realized Equity"] = daily_equity_df["Realized Equity"].fillna(method='ffill')
		daily_equity_df[0] = daily_equity_df[0].fillna(method='ffill')
		# daily_equity_df = daily_equity_df.fillna(0)
		daily_equity_df = daily_equity_df.drop(columns=["Daily Portfolio Equity"])
		self.daily_equity_df = daily_equity_df
		return daily_equity_df
		
	def plot_daily_returns(self):
		fig = go.Figure(data=go.Scatter(x=self.daily_equity_df.index, y=self.daily_equity_df.sum(axis=1)))
		# fig = go.Figure(data=go.Scatter(x=daily_rets.index, y=daily_rets), hover_data={"date": "|%B %d, %Y"})
		# hover_data = {"date": "|%B %d, %Y"},
		
		# title = 'custom tick labels with ticklabelmode="period"')
		fig.update_xaxes(dtick="M1", tickformat="%b\n%Y")
		fig.update_xaxes(rangeslider_visible=True)
		# fig.write_html('first_figure.html', auto_open=True)
		# daily_rets.plot()
		fig.show()
		# plt.grid(True)
		plt.show()
	
	# portfolio.open_orders.open_pos_daily_rets
		
		
	# def plot_daily_returns(self):
	# 	pass
	#
		
		# self._history_dt_idx_range =  pd.date_range(self.acc_details.start_date, self.acc_details.end_date)
		# self._history_dt_idx_range =  pd.bdate_range(self.acc_details.start_date, self.acc_details.end_date)
		# self.open_orders = None
		# self.closed_orders = None
		# self.deposits = None
		# self.wd = None
		# self.wdf = None
		# self.rof = None
		# self.deposits = None
	
	# @property
	# def acc_details(self):
	# 	return self._acc_details


if __name__ == "__main__":
	import pandas as pd
	from src import order_book
	pd.set_option('display.max_rows', 500)
	pd.set_option('display.max_columns', 500)
	pd.set_option('display.width', 500)
	# portfolio_xlsx_file_name = "eToroAccountStatement.xlsx"
	portfolio_xlsx_file_name = "eToroAccountStatementLatest.xlsx"
	portfolio = Portfolio(portfolio_xlsx_file_name)
	# print(f"\nAccount Details:\n {portfolio.acc_details}")
	# print(f"\nClosed Orders:\n {portfolio.closed_orders}")
	print(f"\nOpen Orders:\n {portfolio.open_orders}")
	# print(portfolio.open_orders)
	# print(f"portfolio.acc_details.start_date: {portfolio.acc_details.start_date}")
	# print(f"portfolio.acc_details.end_date: {portfolio.acc_details.end_date}")
	portfolio.closed_orders.plot_daily_returns()
	print(portfolio.closed_orders.pos_daily_returns_df)
	print(portfolio._build_datetime_index())
	print(portfolio._build_daily_realized_equity_df())
	print(portfolio._build_daily_total_realized_equity())
	x = portfolio._build_daily_total_realized_equity()
	y = portfolio._build_daily_realized_equity_df()
	r1 = portfolio.open_orders.pos_daily_returns_df
	r2 = portfolio.open_orders.open_pos_daily_rets
	print(r1)
	print(r2)
	order_book = order_book.OrderBook()
	order_book._add_closed_orders(portfolio.closed_orders.closed_orders_df)
	order_book._add_open_orders(portfolio.open_orders.open_orders_df)
	order_book.build_order_book()
# print(portfolio._extract_transactions_report_realized_equity_df())
	
	
	# portfolio.closed_orders.closed_orders_df["Open Date"].apply(lambda dt_str: utils.standardize_dt_str_format(dt_str))
