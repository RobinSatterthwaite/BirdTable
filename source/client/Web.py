
import json
import cherrypy
import pystache
from datetime import datetime, timezone

from db.Table import Table as DbTable
from db.SiteEntry import SiteEntry
from db.VisitEntry import VisitEntry
from db.SightingEntry import SightingEntry

from client.pages.Home import Home
from client.pages.List import List
from client.pages.Records import Records

from .SpeciesList import SpeciesList


class Web(object):

	def __init__(self, db_conn):
		self.renderer = pystache.Renderer()
		
		self.speciesList = SpeciesList(db_conn)
		self.sites = DbTable("site", SiteEntry, db_conn)
		self.visits = DbTable("visit", VisitEntry, db_conn)
		self.sightings = DbTable("sighting", SightingEntry, db_conn)
		
		self.homePage = Home()

	@cherrypy.expose
	def index(self):
		return self.renderer.render(self.homePage)

	@cherrypy.expose
	def list(self, **kwargs):
		species_list = self.speciesList.getList(kwargs)
		sites_list = self.sites.newContext().fetchAll()
		list_page = List(self.renderer, species_list, sites_list)
		return self.renderer.render(list_page)

	@cherrypy.expose
	def getList(self, **kwargs):
		species_list = self.speciesList.getList(kwargs)
		return List.SpeciesList(species_list, self.renderer)

	@cherrypy.expose
	def records(self):
		species = self.speciesList.getAllSpecies()
		sites = self.sites.newContext().fetchAll()
		records_page = Records(self.renderer, species, sites)
		return self.renderer.render(records_page)

	@cherrypy.expose
	@cherrypy.tools.json_in()
	def newVisit(self):
		visit_data = cherrypy.request.json

		start_time = datetime.strptime(visit_data["StartTime"], "%Y-%m-%dT%H:%M:%S.%f%z")
		end_time = datetime.strptime(visit_data["EndTime"], "%Y-%m-%dT%H:%M:%S.%f%z")

		visits_ctx = self.visits.newContext()
		sightings_ctx = self.sightings.newContext()

		visit = visits_ctx.new()
		visit.site = visit_data["Site"]
		visit.startTime = start_time.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
		visit.endTime = end_time.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
		visits_ctx.commit()

		sightings_data = visit_data["Sightings"]
		for sighting_data in sightings_data:
			sighting = sightings_ctx.new()
			sighting.visit = visit.primaryKey
			sighting.species = sighting_data["Species"]
			sighting.count = sighting_data["Count"]
			sighting.uncertainty = sighting_data["Uncertainty"]
			sighting.seen = sighting_data["Seen"]
			sighting.heard = sighting_data["Heard"]
			sighting.feral = sighting_data["Feral"]
			sighting.notes = sighting_data["Notes"]

		sightings_ctx.commit()

		cherrypy.response.status = 201

	@cherrypy.expose
	def maps(self):
		return "Maps: TBD"
