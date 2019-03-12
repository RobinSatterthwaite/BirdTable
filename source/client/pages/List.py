
from db.Table import Table as DbTable
from db.SiteEntry import SiteEntry

from .SpeciesElement import SpeciesElement
from .DataListOption import DataListOption


class List(object):
	
	def __init__(self, renderer, db_conn):
		self.renderer = renderer
		
		self.sites = DbTable("site", SiteEntry, db_conn)
		self.allSites = self.sites.newContext().fetchAll()


	@property
	def speciesSelection(self):
		return self.species_selection

	@speciesSelection.setter
	def speciesSelection(self, species_selection):
		self.species_selection = species_selection

		self.maxTimesSeen = max(self.species_selection,
		                        key=lambda s:s['times_seen'])['times_seen']

	
	def speciesList(self):
		species_list = []

		for species in self.speciesSelection:
			el = SpeciesElement(
				species['common_name'],
				species['binomial_name'],
				species['count'],
				species['times_seen'],
				(self.maxTimesSeen > 1),
				species['seen'],
				species['heard'])
			species_list.append(self.renderer.render(el))

		return "".join(species_list)


	def speciesCount(self):
		return len(self.speciesSelection)


	def siteListOptions(self):
		site_list = []
		for site in self.allSites:
			site_list.append(self.renderer.render(DataListOption(site.name)))

		return "".join(site_list)


	def countyListOptions(self):
		county_list = []
		for county in ["Berkshire", "Gloucestershire", "Hampshire"]:
			county_list.append(self.renderer.render(DataListOption(county)))

		return "".join(county_list)


	def countryListOptions(self):
		country_list = []
		for country in ["England", "Scotland", "Wales"]:
			country_list.append(self.renderer.render(DataListOption(country)))

		return "".join(country_list)
