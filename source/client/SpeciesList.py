
from datetime import datetime, timezone, timedelta

from db.Table import Table as DbTable
from db.SpeciesEntry import SpeciesEntry


class SpeciesList(object):
	
	def __init__(self, db_conn):
		self.dbConn = db_conn
		
		cursor = self.dbConn.cursor()
		cursor.execute("call get_taxonomic_order()")
		
		order_dict = {}
		i = 0
		for row in cursor:
			order_dict[row.pk] = i
			i += 1
		self.taxonomicOrder = order_dict

		cursor.close()

		self.list = []


	def getList(self, query_args):
		self.list = []
		cursor = self.dbConn.cursor()

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

		query_params = (
			start_date_time,
			end_date_time,
			None,
			include_feral)
		
		cursor.execute("call get_list(?, ?, ?, ?)", query_params)
		field_names = [field[0] for field in cursor.description]

		for row in cursor:
			d = dict(zip(field_names, row))
			d['order'] = self.taxonomicOrder[row.pk]
			self.list.append(d)
		self.list.sort(key=lambda d:d['order'])
		
		cursor.close()
