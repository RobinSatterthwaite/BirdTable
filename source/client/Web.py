
import cherrypy
import pystache

from db.Table import Table as DbTable
from db.SiteEntry import SiteEntry

from client.pages.Home import Home
from client.pages.List import List
from client.pages.Records import Records
from client.pages.recordstable.RecordsTable import RecordsTable
from client.pages.viewvisitrecordoverlay.ViewVisitRecordOverlay import ViewVisitRecordOverlay

from .SpeciesList import SpeciesList
from .VisitRecords import VisitRecords
from .SiteTree import SiteTree


class Web(object):

	def __init__(self, db_conn):
		self.renderer = pystache.Renderer()
		
		self.speciesList = SpeciesList(db_conn)
		self.visitRecords = VisitRecords(db_conn)
		self.sites = DbTable("site", SiteEntry, db_conn)
		self.allSpecies = self.speciesList.getAllSpecies()
		self.siteTree = SiteTree(db_conn)
		
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
	def records(self, **kwargs):
		sites_list = self.sites.newContext().fetchAll()
		records_page = Records(self.renderer, self.allSpecies, sites_list)
		return self.renderer.render(records_page)


	@cherrypy.expose
	def getRecords(self, **kwargs):
		visits, total_visits = self.visitRecords.getRecords(kwargs)
		records = RecordsTable(self.renderer, self.allSpecies, visits, total_visits)
		return self.renderer.render(records)


	@cherrypy.expose
	def getVisitRecord(self, **kwargs):
		visit = self.visitRecords.getRecord(kwargs.get("visitId"))
		visit_record = ViewVisitRecordOverlay(self.renderer, visit, self.allSpecies)
		return self.renderer.render(visit_record)


	@cherrypy.expose
	@cherrypy.tools.json_in()
	def newVisit(self):
		self.visitRecords.newVisit(cherrypy.request.json)
		cherrypy.response.status = 201


	@cherrypy.expose
	def maps(self):
		return "Maps: TBD"
