
from pystache import TemplateSpec


class SpeciesElement(TemplateSpec):

	template_name = "SpeciesElement"

	def __init__(self, name, binomial_name, count, times_seen, seen, heard):
		self.name = name
		self.binomialName = binomial_name
		self.count = count
		self.timesSeen = times_seen
		
		if seen:
			self.seen = "\u26ab"
		else:
			self.seen = ""
		
		if heard:
			self.heard = "\u26ab"
		else:
			self.heard = ""