
from pystache import TemplateSpec

from .SpeciesEntry import SpeciesEntry
from client.pages.DataListOption import DataListOption


class NewEditVisitRecordOverlay(TemplateSpec):

	template_name = "NewEditVisitRecordOverlay"

	def __init__(self, renderer, species, sites):
		self.renderer = renderer
		self.species = species
		self.sites = sites


	def speciesEntries(self):
		species_entries = []

		for species in self.species:
			entry = SpeciesEntry(
				species['pk'],
				species['common_name'])
			species_entries.append(self.renderer.render(entry))

		return "".join(species_entries)


	def siteListOptions(self):
		site_list = []
		for site in self.sites:
			site_option = DataListOption(site.id, site.name)
			site_list.append(self.renderer.render(site_option))

		return "".join(site_list)
