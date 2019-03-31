
from pystache import TemplateSpec


class NewVisitSpeciesEntry(TemplateSpec):

	template_name = "NewVisitSpeciesEntry"

	def __init__(self, id, name):
		self.id = id
		self.name = name

	def speciesId(self):
		return self.id

	def speciesName(self):
		return self.name

	def idPrefix(self):
		return self.id
