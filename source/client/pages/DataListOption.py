
from pystache import TemplateSpec


class DataListOption(TemplateSpec):

	template_name = "DataListOption"

	def __init__(self, value):
		self.value = value
