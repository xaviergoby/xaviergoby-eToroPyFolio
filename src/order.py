

class Order:
	
	def __init__(self, pos_id, symbol, open_price, units, open_datetime, close_price=None, close_datetime=None, leverage=None, amount=None):
		self.pos_id = pos_id
		self.symbol = symbol
		self.open_price = open_price
		self.units = units
		self.open_datetime = open_datetime
		self.close_datetime = close_datetime
		self.close_price = close_price
		self.closed = False if self.close_datetime is None else True
		self.amount = self.open_price * self.units if amount is None else amount
		self.leverage = leverage
		self.daily_profit_df = None
		self.fin_instrument_type = None
	
	def __str__(self):
		info = f"Position ID: {self.pos_id}\n" \
		       f"Symbol: {self.symbol}\n" \
		       f"Open Price: {self.open_price}[$]\n" \
		       f"Units: {self.units}\n" \
		       f"Open Date & Time: {self.open_datetime}\n" \
		       f"Close Date & Time: {self.close_datetime}\n" \
		       f"Close Price: {self.close_price}[$]\n" \
		       f"Amount: {self.amount}[$]\n" \
		       f"Leverage: {self.leverage}[$]\n"
		return info
	
	def __repr__(self):
		info = f"Position ID: {self.pos_id}\n" \
		       f"Symbol: {self.symbol}\n" \
		       f"Open Price: {self.open_price}[$]\n" \
		       f"Units: {self.units}\n" \
		       f"Open Date & Time: {self.open_datetime}\n" \
		       f"Close Date & Time: {self.close_datetime}\n" \
		       f"Close Price: {self.close_price}[$]\n" \
		       f"Amount: {self.amount}[$]\n" \
		       f"Leverage: {self.leverage}[$]\n"
		return info
	
	@property
	def pnl(self):
		if self.daily_profit_df is None:
			return None
		else:
			return float(self.daily_profit_df.values[-1])
