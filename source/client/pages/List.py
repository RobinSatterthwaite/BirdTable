
from .SpeciesElement import SpeciesElement
from .DataListOption import DataListOption


class List(object):
	
	def __init__(self, renderer, species_selection, sites):
		self.renderer = renderer
		
		self.speciesSelection = species_selection
		self.sites = sites

	
	def SpeciesList(species_selection, renderer):
		species_list = []

		max_times_seen = max(species_selection,
		                     key=lambda s:s['times_seen'])['times_seen']

		for species in species_selection:
			el = SpeciesElement(
				species['common_name'],
				species['binomial_name'],
				species['count'],
				species['times_seen'],
				(max_times_seen > 1),
				species['seen'],
				species['heard'])
			species_list.append(renderer.render(el))

		return "".join(species_list)


	def speciesList(self):
		return List.SpeciesList(self.speciesSelection, self.renderer)


	def speciesCount(self):
		return len(self.speciesSelection)


	def siteListOptions(self):
		site_list = []
		for site in self.sites:
			site_option = DataListOption(site.primaryKey, site.name)
			site_list.append(self.renderer.render(site_option))

		return "".join(site_list)


	# def countyListOptions(self):
	# 	county_list = []
	# 	for county in ["Berkshire", "Gloucestershire", "Hampshire"]:
	# 		county_list.append(self.renderer.render(DataListOption(county)))
	# 		
	# 	return "".join(county_list)
	# 	
	# 	
	# def countryListOptions(self):
	# 	country_list = []
	# 	for country in ["England", "Scotland", "Wales"]:
	# 		country_list.append(self.renderer.render(DataListOption(country)))
	# 		
	# 	return "".join(country_list)
