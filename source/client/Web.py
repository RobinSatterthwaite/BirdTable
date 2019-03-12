
import json
import cherrypy
import pystache

from .SpeciesList import SpeciesList

from client.pages.Home import Home
from client.pages.List import List


class Web(object):

	def __init__(self, db_conn):
		self.renderer = pystache.Renderer()
		self.dbConn = db_conn
		self.homePage = Home()
		self.listPage = List(self.renderer, self.dbConn)
		self.speciesList = SpeciesList(db_conn)

	@cherrypy.expose
	def index(self):
		return self.renderer.render(self.homePage)

	@cherrypy.expose
	def list(self, **kwargs):
		self.speciesList.getList(kwargs)
		self.listPage.speciesSelection = self.speciesList.list
		return self.renderer.render(self.listPage)

	@cherrypy.expose
	def getList(self, **kwargs):
		self.speciesList.getList(kwargs)
		self.listPage.speciesSelection = self.speciesList.list
		return self.listPage.speciesList()

	@cherrypy.expose
	def records(self):
		return "Records: TBD"

	@cherrypy.expose
	def sites(self):
		return "Sites: TBD"
