import pandas as pd
from src.details import Details

class AccountDetails:
	
	def __init__(self, acc_details_dict):
		self.acc_details_dict = acc_details_dict
		self.wd = None
		self.wdf = None
		self.deposits = None
		self.rof = None
		self.bre = None
		self.ere = None
		self.bue = None
		self.eue = None
		self.tpl = None
		self.date_created = None
		self.start_date = None
		self.end_date = None
		self.current_tot_unrealized_profit = None
		self.current_tot_realized_profit = None
		self._set_acc_details()
	
	def _set_def_acc_details(self):
		for key, val in self.acc_details_dict.items():
			self.__dict__[key] = val
	
	def _set_extra_acc_details(self):
		self.current_tot_unrealized_profit = self.eue - self.ere
		self.current_tot_realized_profit = self.tpl + self.current_tot_unrealized_profit
		
	def _set_acc_details(self):
		self._set_def_acc_details()
		self._set_extra_acc_details()
	
	def __str__(self):
		# //TODO Get self.total_allocated and self.avaialble fixed
		info = f"Date Created(date_created): {self.date_created}\n" \
		       f"Start Date(start_date): {self.start_date}\n" \
		       f"End Date (end_date): {self.end_date}\n" \
		       f"Beginning Realized Equity (bre): {self.bre}[$]\n" \
		       f"Beginning Unrealized Equity (bue): {self.bue}[$]\n" \
		       f"Deposits (deposits): {self.deposits}[$]\n" \
		       f"Trade Profit Or Loss (Closed positions only) (tpl): {self.tpl}[$]\n" \
		       f"Withdrawals (wd): {self.wd}[$]\n" \
		       f"Withdrawal Fees (wdf): {self.wdf}[$]\n" \
		       f"Total of Withdrawals (tot_wd=wd+wdf): {self.wd + self.wdf}[$]\n" \
		       f"Rollover Fees (rof): {self.rof}[$]\n" \
		       f"Ending Realized Equity (er)(Total Allocated+Available): {self.ere}[$]\n" \
		       f"Ending Unrealized Equity (eue)('Equity'): {self.eue}[$]\n" \
		       f"{'#' * 20} Extra Insights {'#' * 20}\n" \
		       f"Current Total Unrealized Profit (=eue-ere)('Profit'): {round(self.current_tot_unrealized_profit,2)}[$]\n" \
		       f"Current Total Realized Profit (=tpl+eue-ere): {round(self.current_tot_realized_profit,2)}[$]\n"
			   # f"Current Unrealized Profit ('Profit'): {self.current_tot_unrealized_profit}[$]\n" \
		       # f"Current Amount Invested ('Total Allocated'): {self.total_allocated}[$]\n" \
		       # f"Current Balance Available ('Available'): {self.available}[$]\n"
		return info
	
	def __repr__(self):
		# //TODO Get self.total_allocated and self.avaialble fixed
		info = f"Date Created(date_created): {self.date_created}\n" \
		       f"Start Date(start_date): {self.start_date}\n" \
		       f"End Date (end_date): {self.end_date}\n" \
		       f"Beginning Realized Equity (bre): {self.bre}[$]\n" \
		       f"Beginning Unrealized Equity (bue): {self.bue}[$]\n" \
		       f"Deposits (deposits): {self.deposits}[$]\n" \
		       f"Trade Profit Or Loss (Closed positions only) (tpl): {self.tpl}[$]\n" \
		       f"Withdrawals (wd): {self.wd}[$]\n" \
		       f"Withdrawal Fees (wdf): {self.wdf}[$]\n" \
		       f"Total of Withdrawals (tot_wd=wd+wdf): {self.wd + self.wdf}[$]\n" \
		       f"Rollover Fees (rof): {self.rof}[$]\n" \
		       f"Ending Realized Equity (er)(Total Allocated+Available): {self.ere}[$]\n" \
		       f"Ending Unrealized Equity (eue)('Equity'): {self.eue}[$]\n" \
		       f"{'#' * 20} Extra Insights {'#' * 20}\n" \
		       f"Current Total Unrealized Profit (=eue-ere)('Profit'): {round(self.current_tot_unrealized_profit, 2)}[$]\n" \
		       f"Current Total Realized Profit (=tpl+eue-ere): {round(self.current_tot_realized_profit, 2)}[$]\n"
		# f"Current Unrealized Profit ('Profit'): {self.current_tot_unrealized_profit}[$]\n" \
		# f"Current Amount Invested ('Total Allocated'): {self.total_allocated}[$]\n" \
		# f"Current Balance Available ('Available'): {self.available}[$]\n"
		return info


# #//TODO Get self.total_allocated and self.avaialble fixed then delete this line and uncommonet the 3 below
