
from datetime import datetime

from pystache import TemplateSpec


class VisitRecord(TemplateSpec):

	template_name = "VisitRecord"

	def __init__(self, visit, species):
		self.visit = visit
		self.species = species


	def date(self):
		return self.visit['start_time'].strftime("%Y-%m-%dT%H:%M:%SZ")


	def site(self):
		return self.visit['site_name']


	def sightings(self):
		sightings_list = []
		sightings = self.visit['sightings']

		for species in self.species:
			species_pk = species['pk']
			if species_pk in sightings:
				count = sightings[species_pk]['count']
				sightings_list.append("<div>{0}</div>".format(count))
			else:
				sightings_list.append("<div>&nbsp;</div>")

		return "".join(sightings_list)