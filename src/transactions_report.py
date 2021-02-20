


class TransactionsReport:
	
	def __init__(self, transactions_report_df):
		self.transactions_report_df = transactions_report_df
		
	# Deposit, Withdraw Fee, Withdraw Request, Rollover Fee
	# print(portfolio.acc_statement_parser.transactions_report_sheet_df.loc[portfolio.acc_statement_parser.transactions_report_sheet_df['Type'].isin(['Withdraw Request', 'Withdraw Fee'])])
	# self._closed_orders_dict = None
	# pass
	
	def __str__(self):
		return str(self.transactions_report_df)
