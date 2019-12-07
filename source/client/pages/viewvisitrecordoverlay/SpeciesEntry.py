
from pystache import TemplateSpec


class SpeciesEntry(TemplateSpec):

	template_name = "SpeciesEntry"

	def __init__(self, species, sighting, index):
		self.index = index
		self.speciesId = species['pk']
		self.speciesName = species['common_name']
		self.count = sighting['count']
		self.uncertainty = sighting['uncertainty']
		self.isUncertaintyMoreThanZero = self.uncertainty > 0
		self.notes = sighting['notes']
		self.isSeen = sighting['seen'] == 1
		self.isHeard = sighting['heard'] == 1
		self.isFeral = sighting['feral'] == 1
