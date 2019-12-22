
import pyodbc as odbc


class SiteLeaf(object):

	def __init__(self, name, pk):
		self.name = name
		self.id = pk



class SiteNode(object):

	def __init__(self, name, pk):
		self.name = name
		self.id = pk
		self.branches = []


	def getSites(self):
		leaves = []

		for branch in self.branches:
			if isinstance(branch, SiteNode):
				leaves.extend(branch.getSites())
			else:
				leaves.append(branch)

		return leaves


	def getSitesFromNode(self, node_pk):
		leaves = []

		if node_pk is self.id:
			leaves.extend(self.getSites())
		else:
			for branch in self.branches:
				if isinstance(branch, SiteNode):
					leaves.extend(branch.getSitesFromNode(node_pk))

		return leaves


	def getNodes(self):
		nodes = []

		for branch in self.branches:
			if isinstance(branch, SiteNode):
				nodes.append(branch)
				nodes.extend(branch.getNodes())

		return nodes


	def getNodesFromNode(self, node_pk):
		nodes = []

		if node_pk is self.id:
			nodes.extend(self.getNodes)
		else:
			for branch in self.branches:
				if isinstance(branch, SiteNode):
					nodes.extend(branch.getNodesFromNode(node_pk))

		return nodes


	def removeEmptyNodes(self):
		for branch in self.branches:
			if isinstance(branch, SiteNode):
				branch.removeEmptyNodes()

		self.branches[:] = [branch for branch in self.branches if not isinstance(branch, SiteNode) or len(branch.branches) > 0]



class SiteTree(object):

	def __init__(self, db_conn):
		self.dbConn = db_conn

		self.refresh()


	def refresh(self):
		try:
			cursor = self.dbConn.cursor()
			cursor.execute("call get_site_info()")
		except odbc.OperationalError as e:
			sql_state = e.args[0]
			if sql_state == "08003" or sql_state == "08007" or sql_state == "08S01":
				self.dbConn.connect()
				cursor = self.dbConn.cursor()
				cursor.execute("call get_site_info()")

		self.roots = []

		nodes_by_pk = {}
		for row in cursor:
			node = SiteNode(row.name, row.pk)
			nodes_by_pk[row.pk] = node

			if row.parent_fk is None:
				self.roots.append(node)
			else:
				parent = nodes_by_pk[row.parent_fk]
				parent.branches.append(node)

		cursor.nextset()

		for row in cursor:
			if row.area_fk is not None:
				leaf = SiteLeaf(row.name, row.pk)
				parent = nodes_by_pk[row.area_fk]
				parent.branches.append(leaf)

		for root in self.roots:
			if isinstance(root, SiteNode):
				root.removeEmptyNodes()

		self.roots[:] = [root for root in self.roots if not isinstance(root, SiteNode) or len(root.branches) > 0]


	def getSites(self):
		leaves = []

		for root in self.roots:
			if isinstance(root, SiteNode):
				leaves.extend(root.getSites())
			else:
				leaves.append(root)

		return leaves


	def getSitesFromNode(self, node_pk):
		leaves = []

		for root in self.roots:
			if isinstance(root, SiteNode):
				leaves.extend(root.getSitesFromNode(node_pk))

		return leaves


	def getNodes(self):
		nodes = []

		for root in self.roots:
			if isinstance(root, SiteNode):
				nodes.append(root)
				nodes.extend(root.getNodes())

		return nodes


	def getNodesFromNode(self, node_pk):
		nodes = []

		for root in self.roots:
			if isinstance(root, SiteNode):
				nodes.extend(root.getNodesFromNode(node_pk))

		return nodes
