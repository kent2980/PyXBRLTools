from .base import BaseTag


class IxNonNumeric(BaseTag):
    """ 非数値タグの情報を格納するクラス """
    def __init__(self, xbrl_id, context_period, context_entity, context_category, name, xsi_nil, escape, format, text, document_type, report_type):
        self.xbrl_id = xbrl_id
        self.context_period = context_period
        self.context_entity = context_entity
        self.context_category = context_category
        self.name = name
        self.xsi_nil = xsi_nil
        self.escape = escape
        self.format = format
        self.text = text
        self.document_type = document_type
        self.report_type = report_type

    @classmethod
    def keys(cls):
        instance = cls(None, None, None, None, None, None, None, None, None, None, None)
        return list(instance.__dict__)

class IxNonFraction(BaseTag):
    """ 非分数タグの情報を格納するクラス """
    def __init__(self, xbrl_id, context_period, context_entity, context_category, name, unit_ref, xsi_nil, decimals, format, scale, sign, numeric, document_type, report_type):
        self.xbrl_id = xbrl_id
        self.context_period = context_period
        self.context_entity = context_entity
        self.context_category = context_category
        self.name = name
        self.unit_ref = unit_ref
        self.xsi_nil = xsi_nil
        self.decimals = decimals
        self.format = format
        self.scale = scale
        self.sign = sign
        self.numeric = numeric
        self.document_type = document_type
        self.report_type = report_type

    @classmethod
    def keys(cls):
        instance = cls(None, None, None, None, None, None, None, None, None, None, None, None, None, None)
        return list(instance.__dict__)
