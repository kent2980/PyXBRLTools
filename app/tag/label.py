from .base import BaseTag


class LabelValue(BaseTag):
	"""ラベル情報を格納するクラス"""

	def __init__(
		self,
		xlink_type,
		xlink_label,
		xlink_role=None,
		xml_lang=None,
		_id=None,
		label=None,
		xlink_schema=None,
	):
		self.xlink_type = xlink_type
		self.xlink_label = xlink_label
		self.xlink_role = xlink_role
		self.xml_lang = xml_lang
		self.id = _id
		self.label = label
		self.xlink_schema = xlink_schema

	@classmethod
	def keys(cls):
		instance = cls(
			xlink_type=None,
			xlink_label=None,
			xlink_role=None,
			xml_lang=None,
			_id=None,
			label=None,
			xlink_schema=None,
		)
		return list(instance.__dict__)


class LabelLoc:
	"""loc要素情報を格納するクラス"""

	def __init__(self, xlink_type, xlink_label, xlink_schema=None, xlink_href=None):
		self.xlink_type = xlink_type
		self.xlink_label = xlink_label
		self.xlink_schema = xlink_schema
		self.xlink_href = xlink_href

	@classmethod
	def keys(cls):
		instance = cls(
			xlink_type=None,
			xlink_label=None,
			xlink_schema=None,
			xlink_href=None,
		)
		return list(instance.__dict__)


class LabelArc:
	"""arc要素情報を格納するクラス"""

	def __init__(self, xlink_type, xlink_from, xlink_to, xlink_arcrole, xlink_schema):
		self.xlink_type = xlink_type
		self.xlink_from = xlink_from
		self.xlink_to = xlink_to
		self.xlink_arcrole = xlink_arcrole
		self.xlink_schema = xlink_schema

	@classmethod
	def keys(cls):
		instance = cls(
			xlink_type=None,
			xlink_from=None,
			xlink_to=None,
			xlink_arcrole=None,
			xlink_schema=None,
		)
		return list(instance.__dict__)

class LabelRoleRefs:
	"""roleRef要素情報を格納するクラス"""

	def __init__(self, role_uri, xlink_type, xlink_schema, xlink_href):
		self.role_uri = role_uri
		self.xlink_type = xlink_type
		self.xlink_schema = xlink_schema
		self.xlink_href = xlink_href

	@classmethod
	def keys(cls):
		instance = cls(
			role_uri=None,
			xlink_type=None,
			xlink_schema=None,
			xlink_href=None,
		)
		return list(instance.__dict__)

