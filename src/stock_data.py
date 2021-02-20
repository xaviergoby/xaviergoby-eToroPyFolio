import yfinance as yf
import pandas as pd


class SingleStockTicker:
	
	def __init__(self, ticker, start_date=None, end_date=None, period="max", interval='1d', auto_download=True):
		"""
		:param ticker: str of the stock ticker/symbol
		:param start_date: Oldest date YY-MM-DD fstr format
		:param end_date: Most recent date YY-MM-DD fstr format
		:param interval: str of period intervals to get data for, is '1d' by def
		:return:
		"""
		self.ticker = ticker
		self.start_date = start_date
		self.end_date = end_date
		self.period = period
		self.interval = interval
		self.auto_download = auto_download
		self._data = None
		self.open = None
		self.high = None
		self.low = None
		self.close = None
		self.volume = None
		self.period_unit = "".join([s for s in list(self.interval) if s.isalpha()])
		self.period_val = int(float("".join([s for s in list(self.interval) if s.isdigit()])))
		self.stock_data_ohlcv_components = {}
		self._init_yfin_ticker_obj()
		if self.auto_download is True:
			self._build_stock_data_obj()
	
	def __str__(self):
		return "Stock Ticker: {0}\nStart Date (yyy-mm-dd):{1}\nEnd Date (yyy-mm-dd):{2}\nFeatures:{3}".format(self.ticker,
		                                                                                                       self.data.index[0],
		                                                                                                      self.data.index[-1],
		                                                                                                      self.features)
	
	def _init_yfin_ticker_obj(self):
		self.yfin_ticker_obj = yf.Ticker(ticker=self.ticker)
		
	
	def _download_stock_data(self):
		data = self.yfin_ticker_obj.history(start=self.start_date, end=self.end_date, period=self.period, interval=self.interval, actions=False, progress=False)
		data.columns = [col_i.lower() for col_i in data.columns]
		self._data = data
		
	def _set_ohlcv_features(self):
		self.features = self._data.columns.to_list()
		for key in self.features:
			setattr(self, key, self._data[key.lower()])
			self.stock_data_ohlcv_components[key.lower()] = self._data[key.lower()]
	
	def _build_stock_data_obj(self):
		self._download_stock_data()
		self._set_ohlcv_features()
	
	@property
	def data(self):
		return self._data
	
	@property
	def num_bars(self):
		return self._data.shape[0]


if __name__ == "__main__":
	docu = SingleStockTicker("DOCU")
	amd = SingleStockTicker("AMD")
	# print(data.data.loc[""])
	print(list(amd.stock_data_ohlcv_components.keys()))
	
	nvda = yf.Ticker(ticker="NVDA").history(start='2020-12-14', end='2020-12-15', interval="1m")
	nvda.index.tz_convert(tz="Europe/Amsterdam")
	# t = nvda.index.tz_convert(tz="Europe/Amsterdam").tz_convert(None)
	# t = nvda.index.tz_convert(tz="CET").tz_convert(None).tz_convert(None)
	# BETTER OPT:
	# nvda = yf.Ticker(ticker="NVDA").history(start='2020-12-14', end='2020-12-15', interval="1m")
	# nvda.index = nvda.index.tz_convert(tz="CET").tz_convert(None).strftime("%d/%m/%Y %H:%M")
	print(nvda.head())
	print(nvda.tail())
	nvda.shape
	nvda_time_stamps = [dti.time().strftime("%H:%M") for dti in nvda.index.to_list()]
	nvda.insert(0, "Time Stamps", nvda_time_stamps)
	nvda[nvda["Time Stamps"] == "14:31"]
	"""
										  Position ID	         Action	         Amount	   Units    Open Rate  Close Rate  Spread  Profit	   Open Date	         Close Date
	Acc Statement ["Closed Positions"][0]: 705226797	Buy NVIDIA Corporation	 160.28   0.329414	  486.56	523.76	   0.00	    12.25	20/08/2020 14:30	14/12/2020 14:31
		                          Time Stamps        Open        High         Low       Close    Volume
	Datetime
	2020-12-14 09:30:00-05:00       09:30         523.515015  524.359985  523.099976  523.809998  177188
	2020-12-14 09:31:00-05:00       09:31         523.756714  524.700012  523.219971  523.715027   24583
	"""
	
	nio = yf.Ticker(ticker="NIO").history(start='2020-12-14', end='2020-12-15', interval="1m")
	print(nio.head())
	print(nio.tail())
	nio.shape
	nio_time_stamps = [dti.time().strftime("%H:%M") for dti in nio.index.to_list()]
	nio.insert(0, "Time Stamps", nio_time_stamps)
	nio[nio["Time Stamps"] == "14:30"]
	
	"""
										   Position ID	Action	      Amount	Units	 Open Rate Close Rate Spread	Profit	 Open Date	         Close Date
	Acc Statement ["Closed Positions"][1]: 788253940	Buy Nio Inc.  150.00	3.395970	44.17	 39.98	   0.00	     -14.23  09/11/2020 16:24    14/12/2020 14:30
	
		                          Time Stamps       Open       High        Low      Close      Volume
	Datetime
	2020-12-14 09:30:00-05:00       09:30          39.939999  40.130001  39.820000  39.980000  20600639
	2020-12-14 09:31:00-05:00       09:31          39.980000  40.310001  39.810001  40.299999   6312778
	"""
