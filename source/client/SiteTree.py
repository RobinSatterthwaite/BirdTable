
import pyodbc as odbc


class SiteNode(object):

	def __init__(self, name):
		self.name = name
		self.branches = []



class SiteLeaf(object):

	def __init__(self, name, pk):
		self.name = name
		self.id = pk



class SiteTree(object):

	def __init__(self, db_conn):
		self.dbConn = db_conn

		self.roots = []
		self.refresh()


	def refresh(self):
		try:
			cursor = self.dbConn.cursor()
			cursor.execute("call get_site_info()")
		except odbc.OperationalError as e:
			sql_state = e.args[0]
			if sql_state == "08003" or sql_state == "08007" or sql_state == "08S01":
				self.dbConn.connect()
				cursor = self.dbConn.cursor()
			cursor.execute("call get_site_info()")

		areas_by_pk = {}
		for row in cursor:
			node = SiteNode(row.name)
			areas_by_pk[row.pk] = node

			if row.parent_fk is None:
				self.roots.append(node)
			else:
				parent = areas_by_pk[row.parent_fk]
				parent.branches.append(node)

		cursor.nextset()

		for row in cursor:
			if row.area_fk is not None:
				leaf = SiteLeaf(row.name, row.pk)
				parent = areas_by_pk[row.area_fk]
				parent.branches.append(leaf)
