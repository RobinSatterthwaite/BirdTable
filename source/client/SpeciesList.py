
from datetime import datetime, timezone, timedelta
import pyodbc as odbc

from db.SpeciesEntry import SpeciesEntry


class SpeciesList(object):
	
	def __init__(self, db_conn, site_tree):
		self.dbConn = db_conn
		self.siteTree = site_tree
		
		cursor = self.dbConn.cursor()
		cursor.execute("call get_taxonomic_order()")
		
		order_dict = {}
		i = 0
		for row in cursor:
			order_dict[row.pk] = i
			i += 1
		self.taxonomicOrder = order_dict

		cursor.close()


	def getAllSpecies(self):
		l = []

		try:
			cursor = self.dbConn.cursor()
			cursor.execute("select * from species")
		except odbc.OperationalError as e:
			sql_state = e.args[0]
			if sql_state == "08003" or sql_state == "08007" or sql_state == "08S01":
				self.dbConn.connect()
				cursor = self.dbConn.cursor()
				cursor.execute("select * from species")

		field_names = [field[0] for field in cursor.description]

		for row in cursor:
			d = dict(zip(field_names, row))
			d['order'] = self.taxonomicOrder[row.pk]
			l.append(d)
		l.sort(key=lambda d:d['order'])
		
		cursor.close()

		return l


	def getList(self, query_args):
		l = []

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

		include_feral = query_args.get("includeFeral")
		if include_feral is not None:
			include_feral = int(include_feral)

		site_id_arg = query_args.get("siteId")
		if site_id_arg is None:
			area_id_arg = query_args.get("areaId")
			if area_id_arg is not None:
				site_list = self.siteTree.getSitesFromNode(int(area_id_arg))
				site_id_list = [str(site.id) for site in site_list]
				site_id_arg = ",".join(site_id_list)
				print(site_id_arg)

		query_params = (
			start_date_time,
			end_date_time,
			site_id_arg,
			include_feral)

		try:
			cursor = self.dbConn.cursor()
			cursor.execute("call get_list(?, ?, ?, ?)", query_params)
		except odbc.OperationalError as e:
			sql_state = e.args[0]
			if sql_state == "08003" or sql_state == "08007" or sql_state == "08S01":
				self.dbConn.connect()
				cursor = self.dbConn.cursor()
				cursor.execute("call get_list(?, ?, ?, ?)", query_params)

		field_names = [field[0] for field in cursor.description]

		for row in cursor:
			d = dict(zip(field_names, row))
			d['order'] = self.taxonomicOrder[row.pk]
			l.append(d)
		l.sort(key=lambda d:d['order'])
		
		cursor.close()

		return l
