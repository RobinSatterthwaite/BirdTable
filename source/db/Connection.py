
import pyodbc as odbc


class Cursor(object):

	def __init__(self, cursor):
		self._cursor = cursor

	def execute(self, sql, params):
		self._cursor.execute(sql, params)

	def commit(self):
		self._cursor.commit()

	def fetchone(self):
		return self._cursor.fetchone()

	def fetchall(self):
		return self._cursor.fetchall()


class Connection(object):

	def __init__(self, config):
		self.connectString = ("Driver={{{0}}};".format(config["Driver"])
		                    + "Server={0};".format(config["Server"])
		                    + "Port={0};".format(config["Port"])
		                    + "Database={0};".format(config["Name"])
		                    + "User={0};".format(config["Username"])
		                    + "Password={0};".format(config["Password"]))
		
	def __enter__(self):
		self.connect()
		return self

	def __exit__(self, type, value, traceback):
		self.conn.close()


	def connect(self):
		self.conn = odbc.connect(self.connectString)

		self.conn.setdecoding(odbc.SQL_CHAR, encoding="utf-8")
		self.conn.setdecoding(odbc.SQL_WCHAR, encoding="utf-8")
		self.conn.setencoding("utf-8")


	def cursor(self):
		try:
			cursor = self.conn.cursor()
		except odbc.OperationalError as e:
			sql_state = e.args[0]
			if sql_state == "08003" or sql_state == "08007" or sql_state == "08S01":
				self.connect()
				cursor = self.conn.cursor()

		return cursor