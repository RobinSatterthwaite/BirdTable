
from datetime import datetime, timezone, timedelta
import pyodbc as odbc

from db.Table import Table as DbTable
from db.VisitEntry import VisitEntry
from db.SightingEntry import SightingEntry


class VisitRecords(object):

	def __init__(self, db_conn):
		self.dbConn = db_conn
		self.visits = DbTable("visit", VisitEntry, db_conn)
		self.sightings = DbTable("sighting", SightingEntry, db_conn)


	def newVisit(self, visit_data):
		start_time = datetime.strptime(visit_data["StartTime"], "%Y-%m-%dT%H:%M:%S.%f%z")
		end_time = datetime.strptime(visit_data["EndTime"], "%Y-%m-%dT%H:%M:%S.%f%z")

		visits_ctx = self.visits.newContext()
		sightings_ctx = self.sightings.newContext()

		visit = visits_ctx.new()
		visit.site = visit_data["Site"]
		visit.startTime = start_time.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
		visit.endTime = end_time.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
		visit.notes = visit_data["Notes"]
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


	def getRecords(self, query_args):
		start_date_time = None
		start_date_arg = query_args.get("startDate")
		if start_date_arg is not None:
			start_date = datetime.strptime(start_date_arg, "%Y-%m-%d").astimezone(timezone.utc)
			start_date_time = start_date.strftime("%Y-%m-%d %H:%M:%S")

		end_date_time = None
		end_date_arg = query_args.get("endDate")
		if end_date_arg is not None:
			end_date = datetime.strptime(end_date_arg, "%Y-%m-%d").astimezone(timezone.utc)
			end_date += timedelta(hours=23, minutes=59, seconds=59, milliseconds=999)
			end_date_time = end_date.strftime("%Y-%m-%d %H:%M:%S")

		start_index = 0
		start_index_arg = query_args.get("startIndex")
		if start_index_arg is not None:
			start_index = start_index_arg

		query_params = (
			start_date_time,
			end_date_time,
			query_args.get("siteId"),
			query_args.get("speciesId"),
			query_args.get("numResults"),
			start_index)

		try:
			cursor = self.dbConn.cursor()
			cursor.execute("call get_visits(?, ?, ?, ?, ?, ?)", query_params)
		except odbc.OperationalError as e:
			sql_state = e.args[0]
			if sql_state == "08003" or sql_state == "08007" or sql_state == "08S01":
				self.dbConn.connect()
				cursor = self.dbConn.cursor()
				cursor.execute("call get_visits(?, ?, ?, ?, ?, ?)", query_params)

		visits = {}
		visits_list = []
		field_names = [field[0] for field in cursor.description]
		for row in cursor:
			d = dict(zip(field_names, row))
			d['sightings'] = {}
			visits[d['pk']] = d
			visits_list.append(d)

		cursor.nextset()

		field_names = [field[0] for field in cursor.description]
		for row in cursor:
			d = dict(zip(field_names, row))
			visit_pk = d['visit_pk']
			species_pk = d['species_pk']
			visits[visit_pk]['sightings'][species_pk] = d

		cursor.nextset()

		num_visits = cursor.fetchone()[0]

		return visits_list, num_visits
