
from .RecordsTable import RecordsTable
from .NewVisitDialog import NewVisitDialog


class Records(object):
	
	def __init__(self, renderer, species, sites, visits):
		self.renderer = renderer
		self.species = species

		self._newVisitDialog = NewVisitDialog(renderer, species, sites)
		self._recordsTable = RecordsTable(renderer, species, visits)


	def recordsTableSpeciesNames(self):
		species_names = []
		for species in self.species:
			species_names.append("<div>{0}</div>".format(species['common_name']))
		return "".join(species_names)


	def recordsTable(self):
		return self.renderer.render(self._recordsTable)


	def newVisitDialog(self):
		return self.renderer.render(self._newVisitDialog)
