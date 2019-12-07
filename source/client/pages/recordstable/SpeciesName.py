
from pystache import TemplateSpec


class SpeciesName(TemplateSpec):

	template_name = "SpeciesName"

	def __init__(self, species):
		self.speciesName = species['common_name']
		self.speciesId = species['pk']
