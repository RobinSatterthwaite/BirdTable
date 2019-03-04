
import os
import sys
import json
import csv

import pyodbc as odbc

from db.Table import Table as DbTable
from SpeciesEntry import SpeciesEntry
from SiteEntry import SiteEntry
from VisitEntry import VisitEntry
from SightingEntry import SightingEntry


def main():

	with open("config.json") as cfg_file:
		config = json.load(cfg_file)

	if len(sys.argv) < 2:
		raise RuntimeError("No file specified to import.")

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

	sites = DbTable("site", SiteEntry, conn)
	species = DbTable("species", SpeciesEntry, conn)
	visits = DbTable("visit", VisitEntry, conn)
	sightings = DbTable("sighting", SightingEntry, conn)
	species_ctx = species.newContext()
	sites_ctx = sites.newContext()
	visits_ctx = visits.newContext()
	sightings_ctx = sightings.newContext()

	species_dict = {}
	site_dict = {}

	with open(sys.argv[1], newline='') as data_file:
		rows = list(csv.DictReader(data_file, delimiter=',', quotechar='"'))

		# add species to the species table
		for field in rows[0]:
			if field != "Site" and field != "Date":
				species = species_ctx.new()
				species.commonName = field
				species.binomialName = ""
				species_dict[field] = species

		species_ctx.commit()

		for row in rows:
			try:
				site = site_dict[row["Site"]]

			except KeyError:
				# add new site
				site = sites_ctx.new()
				site.name = row["Site"]
				site_dict[row["Site"]] = site
				sites_ctx.commit()

			visit = visits_ctx.new()
			visit.site = site.primaryKey
			visit.startTime = row["Date"]
			visits_ctx.commit()

			for field in row:
				if field != "Site" and field != "Date" and row[field] != "":
					species = species_dict[field]
					sighting = sightings_ctx.new()
					sighting.visit = visit.primaryKey
					sighting.species = species.primaryKey
					sighting.count = row[field]

		sightings_ctx.commit()



	#herring_gull = species.new()
	#herring_gull.commonName = "Herring gull"
	#herring_gull.binomialName = "Larus argentatus"

	#arctic_tern = species.new()
	#arctic_tern.commonName = "Arctic tern"
	#arctic_tern.binomialName = "Sterna paradisaea"

	#species.commit()

	#print herring_gull.primaryKey
	#print arctic_tern.primaryKey

	#herring_gull = (species_ctx
	#	.where(("common_name =", "Herring gull"))
	#	.fetchAll())
	#print(herring_gull[0].binomialName)

	conn.close()


if __name__ == "__main__":
	main()
