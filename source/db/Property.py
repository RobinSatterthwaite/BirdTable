
from typing import Any


class Property(object):

	def __init__(self, name: str):
		self.name = name
		self.value = None
		self._oldValue = None


	def set(self, value: Any) -> None:
		if not self.updated:
			self._oldValue = self.value
		self.value = value


	@property
	def updated(self) -> bool:
		return self.value != self._oldValue


	def finaliseCommit(self) -> None:
		self._oldValue = self.value


	def rollback(self) -> None:
		self.value = self._oldValue
