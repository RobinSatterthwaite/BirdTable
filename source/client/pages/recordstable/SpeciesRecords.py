
from pystache import TemplateSpec


class SpeciesRecords(TemplateSpec):

	template_name = "SpeciesRecords"

	def __init__(self, species, visits):
		self.species = species
		self.visits = visits


	def speciesName(self):
		return self.species['common_name']


	def sightings(self):
		species_pk = self.species['pk']
		
		sightings_list = []
		for visit in reversed(self.visits):
			sightings = visit['sightings']
			if species_pk in sightings:
				count = sightings[species_pk]['count']
				feral = sightings[species_pk]['feral']
				feral_marker = ""
				if feral is not None and feral > 0:
					feral_marker = "*"
				sightings_list.append("<div>{0}{1}</div>".format(
					count, feral_marker))
			else:
				sightings_list.append("<div>&nbsp;</div>")

		return "".join(sightings_list)
