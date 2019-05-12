
from pystache import TemplateSpec

from .VisitRecord import VisitRecord


class RecordsTable(TemplateSpec):

	template_name = "RecordsTable"

	def __init__(self, renderer, species, visits):
		self.renderer = renderer
		self.species = species
		self.visits = visits


	def speciesNames(self):
		species_names = []
		for species in self.species:
			species_names.append("<div>{0}</div>".format(species['common_name']))
		return "".join(species_names)

	
	def VisitRecords(visits, species, renderer):
		visit_list = []

		for visit in reversed(visits):
			visit_list.append(renderer.render(VisitRecord(visit, species)))
		
		return "".join(visit_list)

	
	def visitRecords(self):
		return RecordsTable.VisitRecords(self.visits, self.species, self.renderer)
