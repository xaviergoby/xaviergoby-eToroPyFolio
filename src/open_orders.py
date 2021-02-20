from src.stock_data import SingleStockTicker
import pandas as pd
import datetime
from src import utils


class OpenOrders:
	
	def __init__(self, open_orders_df   ):
		self.open_orders_df = open_orders_df
		self.instruments = self.open_orders_df["Symbols"].unique().tolist()
		self.pos_ids = self.open_orders_df.index.to_list()
		self._build_instruments_data_src_objs()
		self._build_pos_id_symbols_dict()
		self._build_returns_df()
		self._build_open_pos_daily_returns_df()
	# self._closed_orders_dict = None
	# pass
	
	def __str__(self):
		return str(self.open_orders_df)
		
	def _build_pos_id_symbols_dict(self):
		pos_id_symbols_dict = {}
		for pos_id_i in self.pos_ids:
			pos_id_symbols_dict[pos_id_i] = self.open_orders_df.loc[pos_id_i]["Symbols"]
		self.pos_id_symbols_dict = pos_id_symbols_dict
		
	def _build_instruments_data_src_objs(self):
		instruments_data_src_objs = {}
		for instrument_i in self.instruments:
			instruments_data_src_objs[instrument_i] = SingleStockTicker(instrument_i)
		self.instruments_data_src_objs = instruments_data_src_objs
	
	def _build_returns_df(self):
		pos_daily_returns_dict = {}
		for pos_id, pos_symbol in self.pos_id_symbols_dict.items():
			if pos_symbol != "BTC" and pos_symbol != "SAOC" and pos_symbol != "ADA":
				pos_open_date = utils.extract_dt_date(self.open_orders_df.loc[pos_id]["Open Date"])
				# pos_open_date = datetime.datetime.strptime(self.open_orders_df.loc[pos_id]["Open Date"], "%d/%m/%Y %H:%M").strftime("%Y-%m-%d")
				# pos_close_date = self.instruments_data_src_objs[pos_symbol].data.index[-1].strftime("%Y-%m-%d")
				pos_close_dt_idx = self.instruments_data_src_objs[pos_symbol].data.index[-1]
				pos_units = float(self.open_orders_df.loc[pos_id]["Units"])
				# print(f"Creating Dataframe Copy")
				pos_daily_open_prices_df = self.instruments_data_src_objs[pos_symbol].data.loc[pos_open_date:]["close"].copy()
				# print(f"pos_daily_close_prices_df: {pos_daily_close_prices_df}")
				# print(f'self.closed_orders_df.loc[pos_id]["Open Rate"]: {self.closed_orders_df.loc[pos_id]["Open Rate"]}')
				pos_daily_open_prices_df[0] = self.open_orders_df.loc[pos_id]["Avg Open"]
				# pos_daily_close_prices_df[-1] = self.closed_orders_df.loc[pos_id]["Close Rate"]
				# pos_daily_open_rate = self.closed_orders_df.loc[pos_id]["Open Rate"]
				# pos_daily_close_ate = self.closed_orders_df.loc[pos_id]["Close Rate"]
				# pos_daily_turns = round(pos_daily_close_prices_df.diff().sum() * pos_units, 2)
				pos_daily_turns = pos_daily_open_prices_df.diff() * pos_units
				pos_daily_returns_dict[pos_id] = pos_daily_turns
		# pos_daily_returns_dict[pos_id] = pos_daily_turns.iloc[1:-1]
		pos_daily_returns_df = pd.DataFrame(pos_daily_returns_dict)
		self.pos_daily_returns_df = pos_daily_returns_df
	
	def _build_open_pos_daily_returns_df(self):
		self.open_pos_daily_rets = self.pos_daily_returns_df.sum(axis=1).cumsum()
