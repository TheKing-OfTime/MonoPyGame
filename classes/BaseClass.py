class BaseClass:
	_id = ''
	def __init__(self):
		pass

	def get_id(self) -> str:
		return self._id

	def set_id(self, _id:str):
		self._id = _id