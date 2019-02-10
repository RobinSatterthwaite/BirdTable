
import os
import json

import pyodbc as odbc
import cherrypy
import pystache

from db.Table import Table as DbTable
from SpeciesEntry import SpeciesEntry

from client.pages.Home import Home



class Site(object):

	def __init__(self):
		self.renderer = pystache.Renderer()
		self.home = Home()

	@cherrypy.expose
	def index(self):
		return self.renderer.render(self.home)

	@cherrypy.expose
	def list(self):
		return "List: TBD"

	@cherrypy.expose
	def visits(self):
		return "Visits: TBD"

	@cherrypy.expose
	def sites(self):
		return "Sites: TBD"



def main():

	with open("config.json") as cfg_file:
		config = json.load(cfg_file)

	connect_string = ("Driver={{{0}}};".format(config["Database"]["Driver"])
	                + "Server={0};".format(config["Database"]["Server"])
	                + "Port={0};".format(config["Database"]["Port"])
	                + "Database={0};".format(config["Database"]["Name"])
	                + "User={0};".format(config["Database"]["Username"])
	                + "Password={0};".format(config["Database"]["Password"]))
	
	conn = odbc.connect(connect_string)
	
	conn.setdecoding(odbc.SQL_CHAR, encoding="utf-8")
	conn.setdecoding(odbc.SQL_WCHAR, encoding="utf-8")
	conn.setencoding("utf-8")

	species = DbTable("species", SpeciesEntry, conn)

	species_ctx = species.newContext()

	#herring_gull = species.new()
	#herring_gull.commonName = "Herring gull"
	#herring_gull.binomialName = "Larus argentatus"

	#arctic_tern = species.new()
	#arctic_tern.commonName = "Arctic tern"
	#arctic_tern.binomialName = "Sterna paradisaea"

	#species.commit()

	#print herring_gull.primaryKey
	#print arctic_tern.primaryKey

	herring_gull = (species_ctx
		.where(("common_name =", "Herring gull"))
		.fetchAll())
	print(herring_gull[0].binomialName)

	cherrypy.quickstart(Site(), '/', {
		'/': {
			'tools.sessions.on': True,
			'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
		'/assets': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './web/assets'
		}
	})

	conn.close()


if __name__ == "__main__":
	main()
