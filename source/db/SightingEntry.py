
from .Entry import Entry as DbEntry
from .Property import Property as DbProperty


class SightingEntry(DbEntry):

	def __init__(self, row=None):
		super(SightingEntry, self).__init__("sighting")

		self._species = DbProperty("species_fk")
		self.properties.append(self._species)

		self._visit = DbProperty("visit_fk")
		self.properties.append(self._visit)

		self._count = DbProperty("count")
		self.properties.append(self._count)

		if row != None:
			self._primaryKey.value = row.pk
			self._species.value = row.species_fk
			self._visit.value = row.visit_fk
			self._count.value = row.count


	@property
	def species(self):
		return self._species.value

	@species.setter
	def species(self, species):
		self._species.set(species)

	@property
	def visit(self):
		return self._visit.value

	@visit.setter
	def visit(self, visit):
		self._visit.set(visit)
	
	@property
	def count(self):
		return self._count.value

	@count.setter
	def count(self, count):
		self._count.set(count)
