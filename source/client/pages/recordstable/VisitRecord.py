
from datetime import datetime

from pystache import TemplateSpec


class VisitRecord(TemplateSpec):

	template_name = "VisitRecord"

	def __init__(self, visit, species, species_set):
		self.visit = visit
		self.sightingsList = []

		for particular_species in species:
			species_id = particular_species['pk']
			sightings = self.visit['sightings']
			if species_id in sightings:
				count = sightings[species_id]['count']
				feral = sightings[species_id]['feral']

				feral_marker = ""
				if feral is not None and feral > 0:
					feral_marker = "*"
				
				self.sightingsList.append("<div>{0}{1}</div>".format(
					count, feral_marker))
			
			elif species_id in species_set:
				self.sightingsList.append("<div>&nbsp;</div>")


	def visitId(self):
		return self.visit['pk']


	def date(self):
		return self.visit['start_time'].strftime("%Y-%m-%dT%H:%M:%SZ")


	def site(self):
		return self.visit['site_name']


	def sightings(self):
		return "".join(self.sightingsList)