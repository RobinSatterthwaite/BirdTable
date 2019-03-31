
import os
import json

import cherrypy

from db.Connection import Connection as DbConnection
from client.Web import Web


def main():

	with open("config.json") as cfg_file:
		config = json.load(cfg_file)

	with DbConnection(config["Database"]) as conn:

		cherrypy.quickstart(Web(conn), '/', {
			'/': {
				'tools.sessions.on': True,
				'tools.staticdir.root': os.path.abspath(os.getcwd())
			},
			'/assets': {
				'tools.staticdir.on': True,
				'tools.staticdir.dir': './web/assets'
			}
		})


if __name__ == "__main__":
	main()
