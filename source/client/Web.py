
import cherrypy
import pystache

from client.pages.Home import Home
from client.pages.List import List


class Web(object):

	def __init__(self, db_conn):
		self.renderer = pystache.Renderer()
		self.dbConn = db_conn
		self.homePage = Home()

	@cherrypy.expose
	def index(self):
		return self.renderer.render(self.homePage)

	@cherrypy.expose
	def list(self, **kwargs):
		self.listPage = List(self.renderer, self.dbConn, kwargs)
		return self.renderer.render(self.listPage)

	@cherrypy.expose
	def getList(self, **kwargs):
		return self.listPage.getList(kwargs)

	@cherrypy.expose
	def visits(self):
		return "Visits: TBD"

	@cherrypy.expose
	def sites(self):
		return "Sites: TBD"
