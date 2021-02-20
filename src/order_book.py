from src import utils
import pandas as pd
from src.order import Order
from src.stock_data import SingleStockTicker

		
class OrderBook:
	
	def __init__(self):
		self.orders = []
		self.closed_orders = []
		self.open_orders = []
		self.traded_symbols = []
		self._orders_pos_id_obj_dict = {}
		self._closed_orders_pos_id_obj_dict = {}
		self._open_orders_pos_id_obj_dict = {}
	
	def __str__(self):
		return str(self.orders)
	
	def __getitem__(self, pos_id):
		return self._orders_pos_id_obj_dict[pos_id]
	
	
	def _add_closed_order(self, closed_order):
		pos_id = int(closed_order.name)
		symbol = closed_order["Symbols"]
		open_price = float(closed_order["Open Rate"])
		units = float(closed_order["Units"])
		open_datetime = closed_order["Open Date"]
		close_datetime = closed_order["Close Date"]
		close_price = float(closed_order["Close Rate"])
		if pd.isna(closed_order["Leverage"]) is False and closed_order["Leverage"] != 1.0:
			leverage = float(closed_order["Leverage"])
		elif pd.isna(closed_order["Leverage"]) is False and closed_order["Leverage"] == 1.0:
			leverage = 1.0
		else:
			leverage = 1.0
		amount = float(closed_order["Amount"])
		closed_order_obj = Order(pos_id, symbol, open_price, units, open_datetime, close_price=close_price, close_datetime=close_datetime, leverage=leverage, amount=amount)
		self.orders.append(closed_order_obj)
		self._orders_pos_id_obj_dict[pos_id] = closed_order_obj
		self.closed_orders.append(closed_order_obj)
		self._closed_orders_pos_id_obj_dict[pos_id] = closed_order_obj
	
	def _add_open_order(self, open_order):
		pos_id = int(open_order.name)
		symbol = open_order["Symbols"]
		open_price = float(open_order["Avg Open"])
		units = float(open_order["Units"])
		open_datetime = open_order["Open Date"]
		open_order_obj = Order(pos_id, symbol, open_price, units, open_datetime)
		self.orders.append(open_order_obj)
		self._orders_pos_id_obj_dict[pos_id] = open_order_obj
		self.open_orders.append(open_order_obj)
		self._open_orders_pos_id_obj_dict[pos_id] = open_order_obj
	
	def _add_closed_orders(self, closed_orders):
		for df_idx_i in closed_orders.index:
			if closed_orders.loc[df_idx_i]["Symbols"] != "BTC" and closed_orders.loc[df_idx_i]["Symbols"] != "ADA" and closed_orders.loc[df_idx_i]["Symbols"] != "SAOC":
				self._add_closed_order(closed_orders.loc[df_idx_i])
	
	def _add_open_orders(self, open_orders):
		for df_idx_i in open_orders.index:
			self._add_open_order(open_orders.loc[df_idx_i])
	
	@property
	def symbols(self):
		symbols = pd.unique([order_i.symbol for order_i in self.orders])
		return symbols
	
	def _build_symbols_data_src_objs(self):
		symbols_data_src_objs = {}
		for symbol_i in self.symbols:
			symbols_data_src_objs[symbol_i] = SingleStockTicker(symbol_i)
		self.symbols_data_src_objs = symbols_data_src_objs
		
	def _set_orders_daily_profit(self):
		for closed_order_i in self.closed_orders:
			open_date_str = utils.extract_dt_date(str(closed_order_i.open_datetime))
			close_date_str = utils.extract_dt_date(str(closed_order_i.close_datetime))
			closed_order_i_daily_close_df = self.symbols_data_src_objs[closed_order_i.symbol].data.loc[open_date_str:close_date_str]["close"].copy()
			closed_order_i_daily_close_df.iloc[0] = closed_order_i.open_price
			closed_order_i_daily_close_df.iloc[-1] = closed_order_i.close_price
			closed_order_i_daily_close_df = closed_order_i_daily_close_df.diff() * closed_order_i.units
			closed_order_i.daily_profit_df = closed_order_i_daily_close_df.cumsum()
			
			
			# closed_order_i.daily_profit_df = self.symbols_data_src_objs[closed_order_i.symbol].data.loc[open_date_str:close_date_str]["close"].copy() * closed_order_i.units
			# closed_order_i.daily_profit_df.iloc[0] = closed_order_i.open_price * closed_order_i.units
			# closed_order_i.daily_profit_df.iloc[-1] = closed_order_i.close_price * closed_order_i.units
			# closed_order_i.daily_profit_df = closed_order_i.daily_profit_df.diff().cumsum()
			
		for open_order_i in self.open_orders:
			open_date_str = utils.extract_dt_date(str(open_order_i.open_datetime))
			open_order_i.daily_profit_df = self.symbols_data_src_objs[open_order_i.symbol].data.loc[open_date_str:]["close"].copy() * open_order_i.units
			open_order_i.daily_profit_df.iloc[0] = open_order_i.open_price * open_order_i.units
			open_order_i.daily_profit_df = open_order_i.daily_profit_df.diff().cumsum()
			
	@property
	def orders_daily_returns_df(self):
		rets = pd.concat([order_i.daily_profit_df for order_i in self.orders], axis=1).fillna(0)
		rets.columns = [order_i.pos_id for order_i in self.orders]
		return rets
	
	@property
	def closed_orders_daily_returns_df(self):
		closed_orders_rets = pd.concat([closed_order_i.daily_profit_df for closed_order_i in self.closed_orders], axis=1).fillna(0)
		closed_orders_rets.columns = [closed_order_i.pos_id for closed_order_i in self.closed_orders]
		return closed_orders_rets
	
	@property
	def open_orders_daily_returns_df(self):
		open_orders_rets = pd.concat([open_order_i.daily_profit_df for open_order_i in self.open_orders], axis=1).fillna(0)
		open_orders_rets.columns = [open_order_i.pos_id for open_order_i in self.open_orders]
		return open_orders_rets
	
	@property
	def daily_returns(self):
		rets = self.orders_daily_returns_df
		tot_rets = rets.sum(axis=1)
		return tot_rets
	
	@property
	def closed_orders_daily_returns(self):
		closed_rets = self.closed_orders_daily_returns_df
		tot_closed_rets = closed_rets.sum(axis=1)
		return tot_closed_rets
	
	@property
	def open_orders_daily_returns(self):
		open_rets = self.open_orders_daily_returns_df
		tot_open_rets = open_rets.sum(axis=1)
		return tot_open_rets

	def build_order_book(self):
		self._build_symbols_data_src_objs()
		self._set_orders_daily_profit()
