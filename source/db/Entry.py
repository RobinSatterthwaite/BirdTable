
from typing import Any
import pyodbc as odbc

from .Property import Property


class Entry(object):

	def __init__(self, table_name: str):
		self._delete = False
		self._tableName = table_name
		self._primaryKey = Property("pk")
		self.properties = [self._primaryKey]


	@property
	def primaryKey(self) -> int:
		return self._primaryKey.value


	def delete(self) -> None:
		self._delete = True


	def _commitInsert(self, cursor: odbc.Cursor) -> None:
		prop_names = ""
		prop_value_tags = ""
		prop_values = []
		for prop in self.properties:
			if prop.value != None:
				if prop_names != "":
					prop_names += ","
					prop_value_tags += ","
				prop_names += prop.name
				prop_value_tags += "?"
				prop_values.append(prop.value)

		cursor.execute("INSERT INTO {0} ({1}) VALUES ({2})"
			               .format(self._tableName, prop_names, prop_value_tags), prop_values)
		cursor.commit()
		cursor.execute("SELECT LAST_INSERT_ID()")
		self._primaryKey.value = cursor.fetchone()[0]


	def _executeUpdate(self, cursor: odbc.Cursor) -> None:
		prop_sets = ""
		prop_values = []
		for prop in self.properties:
			if prop.updated:
				if prop_sets != "":
					prop_sets += ","
				prop_sets += "{0}=?".format(prop.name)
				prop_values.append(prop.value)

		if len(prop_values) > 0:
			prop_values.append(self.primaryKey)

			cursor.execute("UPDATE {0} SET {1} WHERE pk=?"
				               .format(self._tableName, prop_sets), prop_values)


	def _executeDelete(self, cursor: odbc.Cursor) -> None:
		cursor.execute("DELETE FROM {0} WHERE pk=?"
				             .format(self._tableName), self.primaryKey)


	def _finaliseCommit(self) -> None:
		self._delete = False
		for prop in self.properties:
			prop.finaliseCommit()


	def rollback(self) -> None:
		self._delete = False
		for prop in self.properties:
			prop.rollback()
			