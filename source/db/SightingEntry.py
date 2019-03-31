
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

		self._uncertainty = DbProperty("uncertainty")
		self.properties.append(self._uncertainty)

		self._seen = DbProperty("seen")
		self.properties.append(self._seen)

		self._heard = DbProperty("heard")
		self.properties.append(self._heard)

		self._feral = DbProperty("feral")
		self.properties.append(self._feral)

		self._notes = DbProperty("notes")
		self.properties.append(self._notes)

		if row != None:
			self._primaryKey.value = row.pk
			self._species.value = row.species_fk
			self._visit.value = row.visit_fk
			self._count.value = row.count
			self._uncertainty.value = row.uncertainty
			self._seen.value = row.seen
			self._heard.value = row.heard
			self._feral.value = row.feral
			self._notes.value = row.notes


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
	
	@property
	def uncertainty(self):
		return self._uncertainty.value

	@uncertainty.setter
	def uncertainty(self, uncertainty):
		self._uncertainty.set(uncertainty)
	
	@property
	def seen(self):
		return self._seen.value

	@seen.setter
	def seen(self, seen):
		if seen:
			self._seen.set(1)
		else:
			self._seen.set(0)
	
	@property
	def heard(self):
		return self._heard.value

	@heard.setter
	def heard(self, heard):
		if heard:
			self._heard.set(1)
		else:
			self._heard.set(0)
	
	@property
	def feral(self):
		return self._feral.value

	@feral.setter
	def feral(self, feral):
		if feral:
			self._feral.set(1)
		else:
			self._feral.set(0)
	
	@property
	def notes(self):
		return self._notes.value

	@notes.setter
	def notes(self, notes):
		self._notes.set(notes)
