



class Details:
	
	def __init__(self, details_dict):
		self._details_dict = details_dict
		for detail_key, detail_value in self._details_dict.items():
			setattr(self, detail_key, detail_value)
