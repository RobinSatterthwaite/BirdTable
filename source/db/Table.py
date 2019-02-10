
from typing import ClassVar, Sequence
import pyodbc as odbc

from .Entry import Entry
from .SqlStringUtilities import constraintToSql


class TableContext(object):
	"""
	Class for interacting with database table via pyodbc cursor.
	"""

	def __init__(self, table_name: str, entry_class: ClassVar, cursor: odbc.Cursor):
		self._tableName = table_name
		self._entryClass = entry_class
		self._cursor = cursor

		self._newEntries = []
		self._selectedEntries = []
		
		self._whereClause = ""
		self._whereParams = []


	def where(self, constraints) -> 'TableContext':
		"""
		Set the...
		"""
		self._whereClause, self._whereParams = constraintToSql(constraints)
		return self


	def fetchAll(self) -> Sequence:
		"""
		Return the ...
		"""
		statement = "SELECT * FROM {0}".format(self._tableName)
		params = []

		if len(self._whereClause) > 0:
			statement += " WHERE {0}".format(self._whereClause)
			params += self._whereParams

		self._cursor.execute(statement, params)
		rows = self._cursor.fetchall()
		self._selectedEntries = []
		for row in rows:
			entry = self._entryClass(row)
			self._selectedEntries.append(entry)

		return self._selectedEntries
		

	def new(self) -> Entry:
		"""
		Create new Entry object. Entry is only added to database on next call to commit.
		"""
		entry = self._entryClass()
		self._newEntries.append(entry)

		return entry


	def commit(self) -> None:
		"""
		Commit changes to the database.
		"""
		while len(self._newEntries) > 0:
			entry = self._newEntries.pop(0)
			entry._commitInsert(self._cursor)
			self._selectedEntries.append(entry)

		for entry in self._selectedEntries:
			if entry._delete:
				entry._executeDelete(self._cursor)
			else:
				entry._executeUpdate(self._cursor)

		self._cursor.commit()

		# can't delete items while iterating list
		self._selectedEntries[:] = [e for e in self._selectedEntries if not e._delete]

		for entry in self._selectedEntries:
			entry._finaliseCommit()


	def rollback(self) -> None:
		"""
		Rollback changes.  New entry objects remain in scope, but will not be
		commited to the database.
		"""
		self._newEntries = []
		for entry in self._selectedEntries:
			entry.rollback()



class Table(object):
	"""

	"""

	def __init__(self, table_name: str, entry_class: ClassVar, conn: odbc.Connection):
		self._tableName = table_name
		self._entryClass = entry_class
		self._conn = conn


	def newContext(self) -> TableContext:
		"""
		Returns a new context for operating on the database table concurrently with other contexts.
		"""
		return TableContext(self._tableName, self._entryClass, self._conn.cursor())
