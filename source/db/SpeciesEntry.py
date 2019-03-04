
from .Entry import Entry as DbEntry
from .Property import Property as DbProperty


class SpeciesEntry(DbEntry):

	def __init__(self, row=None):
		super(SpeciesEntry, self).__init__("species")

		self._commonName = DbProperty("common_name")
		self.properties.append(self._commonName)

		self._binomialName = DbProperty("binomial_name")
		self.properties.append(self._binomialName)

		self._taxonomicNext = DbProperty("taxonomic_next")
		self.properties.append(self._taxonomicNext)

		self._referenceImage = DbProperty("reference_image")
		self.properties.append(self._referenceImage)

		if row != None:
			self._primaryKey.value = row.pk
			self._commonName.value = row.common_name
			self._binomialName.value = row.binomial_name
			self._taxonomicNext.value = row.taxonomic_next
			self._referenceImage.value = row.reference_image_fk


	@property
	def commonName(self):
		return self._commonName.value

	@commonName.setter
	def commonName(self, name):
		self._commonName.set(name)

	@property
	def binomialName(self):
		return self._binomialName.value

	@binomialName.setter
	def binomialName(self, name):
		self._binomialName.set(name)
	
	@property
	def taxonomicNext(self):
		return self._taxonomicNext.value

	@taxonomicNext.setter
	def taxonomicNext(self, species):
		self._taxonomicNext.set(species)

	@property
	def referenceImage(self):
		return self._referenceImage.value

	@referenceImage.setter
	def referenceImage(self, image):
		self._referenceImage.set(image)
