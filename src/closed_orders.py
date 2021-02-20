import pandas as pd
import matplotlib.pyplot as plt
import datetime
from src.stock_data import SingleStockTicker
import plotly.graph_objects as go

class ClosedOrders:
	
	def __init__(self, closed_orders_df):
		self.closed_orders_df = closed_orders_df
		self.instruments = self.closed_orders_df["Symbols"].unique().tolist()
		self.pos_ids = self.closed_orders_df.index.to_list()
		self._build_instruments_data_src_objs()
		self._build_pos_id_symbols_dict()
		self._build_returns_df()
		self._build_closed_pos_daily_returns_df()
		# self._closed_orders_dict = None
		# pass
	
	def _build_instruments_data_src_objs(self):
		instruments_data_src_objs = {}
		for instrument_i in self.instruments:
			instruments_data_src_objs[instrument_i] = SingleStockTicker(instrument_i)
		self.instruments_data_src_objs = instruments_data_src_objs
		
	def _build_pos_id_symbols_dict(self):
		pos_id_symbols_dict = {}
		for pos_id_i in self.pos_ids:
			pos_id_symbols_dict[pos_id_i] = self.closed_orders_df.loc[pos_id_i]["Symbols"]
		self.pos_id_symbols_dict = pos_id_symbols_dict
		
	def _build_returns_df(self):
		pos_daily_returns_dict = {}
		for pos_id, pos_symbol in self.pos_id_symbols_dict.items():
			if pos_symbol != "BTC" and pos_symbol != "SAOC" and pos_symbol != "ADA":
				pos_open_date = datetime.datetime.strptime(self.closed_orders_df.loc[pos_id]["Open Date"], "%d/%m/%Y %H:%M").strftime("%Y-%m-%d")
				pos_close_date = datetime.datetime.strptime(self.closed_orders_df.loc[pos_id]["Close Date"], "%d/%m/%Y %H:%M").strftime("%Y-%m-%d")
				pos_units = float(self.closed_orders_df.loc[pos_id]["Units"])
				# print(f"Creating Dataframe Copy")
				pos_daily_close_prices_df = self.instruments_data_src_objs[pos_symbol].data.loc[pos_open_date:pos_close_date]["close"].copy()
				# print(f"pos_daily_close_prices_df: {pos_daily_close_prices_df}")
				# print(f'self.closed_orders_df.loc[pos_id]["Open Rate"]: {self.closed_orders_df.loc[pos_id]["Open Rate"]}')
				pos_daily_close_prices_df[0] = self.closed_orders_df.loc[pos_id]["Open Rate"]
				pos_daily_close_prices_df[-1] = self.closed_orders_df.loc[pos_id]["Close Rate"]
				# pos_daily_open_rate = self.closed_orders_df.loc[pos_id]["Open Rate"]
				# pos_daily_close_ate = self.closed_orders_df.loc[pos_id]["Close Rate"]
				# pos_daily_turns = round(pos_daily_close_prices_df.diff().sum() * pos_units, 2)
				pos_daily_turns = pos_daily_close_prices_df.diff() * pos_units
				pos_daily_returns_dict[pos_id] = pos_daily_turns
				# pos_daily_returns_dict[pos_id] = pos_daily_turns.iloc[1:-1]
		pos_daily_returns_df = pd.DataFrame(pos_daily_returns_dict)
		self.pos_daily_returns_df = pos_daily_returns_df
		# return pos_daily_returns_df
				# datetime.datetime.strptime(self.closed_orders.closed_orders_df.loc[718438043]["Open Date"], "%d/%m/%Y %H:%M").strftime("%Y-%m-%d")
			
		
		
# Symbols  Amount  Leverage       Units  Open Rate  Close Rate  Spread  Profit         Open Date        Close Date         TP      SL  Rollover Fees&Dividends  Type
	# Position ID
			
# 718438043      DOCU     NaN    400.00    1.626876     245.87      237.10    0.00  -14.27  03/09/2020 13:30  16/10/2020 15:00    2704.55    0.01                     0.00  Real
	
	def _build_closed_pos_daily_returns_df(self):
		self.closed_pos_daily_rets = self.pos_daily_returns_df.sum(axis=1).cumsum()
	
	def plot_daily_returns(self):
		fig = go.Figure(data=go.Scatter(x=self.closed_pos_daily_rets.index, y=self.closed_pos_daily_rets))
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
		
	
	def __str__(self):
		return str(self.closed_orders_df)
