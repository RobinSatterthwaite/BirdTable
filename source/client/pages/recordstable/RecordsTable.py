
from pystache import TemplateSpec

from .SpeciesName import SpeciesName
from .VisitRecord import VisitRecord


class RecordsTable(TemplateSpec):

	template_name = "RecordsTable"

	def __init__(self, renderer, species, visits, total_num_visits):
		self.renderer = renderer
		self.species = species

		self.totalNumVisits = total_num_visits
		self.speciesSet = set()
		self.visitsList = []

		for visit in reversed(visits):
			for particular_species in self.species:
				species_id = particular_species['pk']
				if species_id in visit['sightings']:
					self.speciesSet.add(species_id)

		for visit in reversed(visits):
			visit_record = VisitRecord(visit, species, self.speciesSet)
			self.visitsList.append(self.renderer.render(visit_record))


	def speciesNames(self):
		species_list = []

		for particular_species in self.species:
			species_id = particular_species['pk']
			if species_id in self.speciesSet:
				species_name = SpeciesName(particular_species)
				species_list.append(self.renderer.render(species_name))

		return "".join(species_list)


	def visitRecords(self):
		return "".join(self.visitsList)
