
from pystache import TemplateSpec

from .NewVisitSpeciesEntry import NewVisitSpeciesEntry
from client.pages.DataListOption import DataListOption


class NewVisitDialog(TemplateSpec):

	template_name = "NewVisitDialog"

	def __init__(self, renderer, species, sites):
		self.renderer = renderer
		self.species = species
		self.sites = sites


	def speciesEntries(self):
		species_entries = []

		for species in self.species:
			entry = NewVisitSpeciesEntry(
				species['pk'],
				species['common_name'])
			species_entries.append(self.renderer.render(entry))

		return "".join(species_entries)


	def siteListOptions(self):
		site_list = []
		for site in self.sites:
			site_option = DataListOption(site.primaryKey, site.name)
			site_list.append(self.renderer.render(site_option))

		return "".join(site_list)
