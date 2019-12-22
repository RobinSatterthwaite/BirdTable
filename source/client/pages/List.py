
from .SpeciesElement import SpeciesElement
from .DataListOption import DataListOption


class List(object):
	
	def __init__(self, renderer, species_selection, site_tree):
		self.renderer = renderer
		
		self.speciesSelection = species_selection
		self.siteTree = site_tree

	
	def SpeciesList(species_selection, renderer):
		species_list = []

		max_times_seen = 0
		if len(species_selection) > 0:
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


	def areaListOptions(self):
		area_list = self.siteTree.getNodes()
		area_options = []
		for area in area_list:
			area_option = DataListOption(area.id, area.name)
			area_options.append(self.renderer.render(area_option))

		return "".join(area_options)


	def siteListOptions(self):
		site_list = self.siteTree.getSites()
		site_options = []
		for site in site_list:
			site_option = DataListOption(site.id, site.name)
			site_options.append(self.renderer.render(site_option))

		return "".join(site_options)


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
