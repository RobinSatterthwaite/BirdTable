
from typing import Union, Tuple, List


def constraintToSql(constraints: Union[Tuple, List]) -> str:
	"""
	Construct SQL constraint string from constraint tuple or list of tuples.
	"""
	if isinstance(constraints, tuple):
		if len(constraints) < 2 or len(constraints) > 3:
			raise ValueError("Constraints tuple must have at least 2 and no more than 3 elements.")

		sql = "{0} ?".format(constraints[0])
		if len(constraints) > 2:
			sql += " {0}".format(constraints[2])

		return sql, [constraints[1]]

	elif isinstance(constraints, list):
		sql = "("
		params = []
		for constraint in constraints:
			constraint_string, constraint_params = constraintToSql(constraint)
			if len(sql) > 1:
				sql += " "
			sql += constraint_string
			params += constraint_params

		sql += ")"

		return sql, params

	else:
		raise TypeError("Constraints must be a constraint tuple or list of constraints.")
