
import cherrypy
import pystache

from client.pages.Home import Home
from client.pages.List import List
from client.pages.Records import Records
from client.pages.recordstable.RecordsTable import RecordsTable
from client.pages.viewvisitrecordoverlay.ViewVisitRecordOverlay import ViewVisitRecordOverlay
from client.pages.DataListOption import DataListOption

from .SpeciesList import SpeciesList
from .VisitRecords import VisitRecords
from .SiteTree import SiteTree


class Web(object):

	def __init__(self, db_conn):
		self.renderer = pystache.Renderer()
		
		self.siteTree = SiteTree(db_conn)
		self.speciesList = SpeciesList(db_conn, self.siteTree)
		self.allSpecies = self.speciesList.getAllSpecies()
		self.visitRecords = VisitRecords(db_conn)
		self.allSites = self.siteTree.getSites()
		
		self.homePage = Home()


	@cherrypy.expose
	def index(self):
		return self.renderer.render(self.homePage)


	@cherrypy.expose
	def list(self, **kwargs):
		species_list = self.speciesList.getList(kwargs)
		list_page = List(self.renderer, species_list, self.siteTree)
		return self.renderer.render(list_page)


	@cherrypy.expose
	def getList(self, **kwargs):
		species_list = self.speciesList.getList(kwargs)
		return List.SpeciesList(species_list, self.renderer)


	@cherrypy.expose
	def records(self, **kwargs):
		records_page = Records(self.renderer, self.allSpecies, self.allSites)
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
	@cherrypy.tools.json_in()
	def editVisit(self, **kwargs):
		visit_pk = kwargs.get("visitId")
		self.visitRecords.editVisit(visit_pk, cherrypy.request.json)


	@cherrypy.expose
	def getSiteOptions(self, **kwargs):
		site_list = self.siteTree.getSitesFromNode(int(kwargs.get("areaId")))
		site_options = []
		for site in site_list:
			site_option = DataListOption(site.id, site.name)
			site_options.append(self.renderer.render(site_option))

		return "".join(site_options)


	@cherrypy.expose
	def getAreas(self, **kwargs):
		self.siteTree.getNodesFromNode(kwargs.get("areaId"))


	@cherrypy.expose
	def maps(self):
		return "Maps: TBD"
