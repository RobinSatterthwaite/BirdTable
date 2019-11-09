
from .Entry import Entry as DbEntry
from .Property import Property as DbProperty


class VisitEntry(DbEntry):

	def __init__(self, row=None):
		super(VisitEntry, self).__init__("visit")

		self._site = DbProperty("site_fk")
		self.properties.append(self._site)

		self._startTime = DbProperty("start_time")
		self.properties.append(self._startTime)

		self._endTime = DbProperty("end_time")
		self.properties.append(self._endTime)

		self._notes = DbProperty("notes")
		self.properties.append(self._notes)

		if row != None:
			self._primaryKey.value = row.pk
			self._site.value = row.site_fk
			self._startTime.value = row.start_time
			self._endTime.value = row.end_time
			self._notes.value = row.notes


	@property
	def site(self):
		return self._site.value

	@site.setter
	def site(self, site_fk):
		self._site.set(site_fk)

	@property
	def startTime(self):
		return self._startTime.value

	@startTime.setter
	def startTime(self, start_time):
		self._startTime.set(start_time)

	@property
	def endTime(self):
		return self._endTime.value

	@endTime.setter
	def endTime(self, end_time):
		self._endTime.set(end_time)

	@property
	def notes(self):
		return self._notes.value

	@notes.setter
	def notes(self, notes_txt):
		self._notes.set(notes_txt)
