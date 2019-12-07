
from datetime import datetime
from pystache import TemplateSpec

from .SpeciesEntry import SpeciesEntry


class ViewVisitRecordOverlay(TemplateSpec):

	template_name = "ViewVisitRecordOverlay"

	def __init__(self, renderer, visit, species):
		self.renderer = renderer
		self.species = species
		self.siteName = visit['site_name']
		self.startTime = visit['start_time'].strftime("%Y-%m-%dT%H:%M:%SZ")
		self.endTime = visit['end_time'].strftime("%Y-%m-%dT%H:%M:%SZ")
		self.notes = visit['notes']
		self.sightings = visit['sightings']


	def speciesEntries(self):
		species_entries = []

		index = 0
		for particular_species in self.species:
			species_id = particular_species['pk']
			if species_id in self.sightings:
				index += 1
				sighting = self.sightings[species_id]
				species_entry = SpeciesEntry(particular_species, sighting, index)
				species_entries.append(self.renderer.render(species_entry))

		return "".join(species_entries)
