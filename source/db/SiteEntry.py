
from .Entry import Entry as DbEntry
from .Property import Property as DbProperty


class SiteEntry(DbEntry):

	def __init__(self, row=None):
		super(SiteEntry, self).__init__("site")

		self._name = DbProperty("name")
		self.properties.append(self._name)

		if row != None:
			self._primaryKey.value = row.pk
			self._name.value = row.name


	@property
	def name(self):
		return self._name.value

	@name.setter
	def name(self, name):
		self._name.set(name)
