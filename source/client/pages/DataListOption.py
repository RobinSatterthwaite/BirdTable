
from pystache import TemplateSpec


class DataListOption(TemplateSpec):

	template_name = "DataListOption"

	def __init__(self, value_id, text_value):
		self.valueId = value_id
		self.textValue = text_value
