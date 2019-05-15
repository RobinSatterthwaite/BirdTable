
from datetime import datetime

from pystache import TemplateSpec


class VisitRecordHeading(TemplateSpec):

	template_name = "VisitRecordHeading"

	def __init__(self, visit):
		self.visit = visit


	def date(self):
		return self.visit['start_time'].strftime("%Y-%m-%dT%H:%M:%SZ")


	def site(self):
		return self.visit['site_name']
