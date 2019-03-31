
from .NewVisitDialog import NewVisitDialog


class Records(object):
	
	def __init__(self, renderer, species, sites):
		self.renderer = renderer

		self._newVisitDialog = NewVisitDialog(renderer, species, sites)


	def newVisitDialog(self):
		return self.renderer.render(self._newVisitDialog)
