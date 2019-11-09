
from pystache import TemplateSpec


class SpeciesRecords(TemplateSpec):

	template_name = "SpeciesRecords"

	def __init__(self, species, visits):
		self.species = species
		self.visits = visits

		self.speciesId = self.species['pk']
		
		self.recordIsEmpty = True
		self.sightingsList = []
		for visit in reversed(self.visits):
			sightings = visit['sightings']
			if self.speciesId in sightings:
				count = sightings[self.speciesId]['count']
				feral = sightings[self.speciesId]['feral']
				feral_marker = ""
				if feral is not None and feral > 0:
					feral_marker = "*"
				self.sightingsList.append("<div>{0}{1}</div>".format(
					count, feral_marker))
				self.recordIsEmpty = False
			else:
				self.sightingsList.append("<div>&nbsp;</div>")


	def speciesName(self):
		return self.species['common_name']


	def sightings(self):
		return "".join(self.sightingsList)
