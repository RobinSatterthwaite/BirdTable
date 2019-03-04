
import os
import json

import pyodbc as odbc
import cherrypy
import pystache

from client.Web import Web


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

	#cursor = conn.cursor()
	#cursor.execute("call get_list('2017-01-01', '2020-01-01', 0)")
	#for row in cursor:
	#	print(row)

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

	conn.close()


if __name__ == "__main__":
	main()
