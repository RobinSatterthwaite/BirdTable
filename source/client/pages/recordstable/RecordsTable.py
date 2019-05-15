
from pystache import TemplateSpec

from .VisitRecordHeading import VisitRecordHeading
from .SpeciesRecords import SpeciesRecords


class RecordsTable(TemplateSpec):

	template_name = "RecordsTable"

	def __init__(self, renderer, species, visits, total_num_visits):
		self.renderer = renderer
		self.species = species
		self.visits = visits
		self.totalNumVisits = total_num_visits


	def visitHeadings(self):
		visits_list = []

		for visit in reversed(self.visits):
			visit_heading = VisitRecordHeading(visit)
			visits_list.append(self.renderer.render(visit_heading))

		return "".join(visits_list)


	def speciesRecords(self):
		species_list = []

		for species in self.species:
			species_records = SpeciesRecords(species, self.visits)
			species_list.append(self.renderer.render(species_records))
		
		return "".join(species_list)
