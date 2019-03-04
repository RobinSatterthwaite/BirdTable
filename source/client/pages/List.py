
from db.Table import Table as DbTable
from db.SiteEntry import SiteEntry

from .SpeciesElement import SpeciesElement
from .DataListOption import DataListOption


class List(object):
	
	def __init__(self, renderer, db_conn, query_args):
		self.renderer = renderer
		self.sites = DbTable("site", SiteEntry, db_conn)

		self.dbConn = db_conn
		self.speciesSelection = self.getList(query_args)
		
		self.allSites = self.sites.newContext().fetchAll()


	def getList(self, query_args):
		species_selection = []
		cursor = self.dbConn.cursor()

		include_feral = query_args.get("includeFeral")
		if include_feral:
			include_feral = int(include_feral)
		query_params = (
			query_args.get("startDate"),
			query_args.get("endDate"),
			None,
			include_feral)
		
		cursor.execute("call get_list(?, ?, ?, ?)", query_params)
		for row in cursor:
			species_selection.append(row)
		cursor.close()

		return species_selection


	def speciesList(self):
		species_list = []
		for species in self.speciesSelection:
			el = SpeciesElement(species.common_name, species.binomial_name, species.count, species.times_seen, species.seen, species.heard)
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
