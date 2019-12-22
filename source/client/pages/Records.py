
from .neweditvisitrecordoverlay.NewEditVisitRecordOverlay import NewEditVisitRecordOverlay


class Records(object):
	
	def __init__(self, renderer, species, sites):
		self.renderer = renderer

		self._newEditVisitRecordOverlay = NewEditVisitRecordOverlay(renderer, species, sites)


	def newEditVisitRecordOverlay(self):
		return self.renderer.render(self._newEditVisitRecordOverlay)
