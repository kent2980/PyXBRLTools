from .base_xbrl_parser import BaseXBRLParser

class SchemaParser(BaseXBRLParser):
    def import_schemas(self):
        lists = []

        tags = self.soup.find_all(name='import')
        for tag in tags:
            dict = {
                'schema_location': tag.get('schemaLocation'),
                'name_space': tag.get('namespace')
            }

            lists.append(dict)

        self.data = lists

        return self

    def link_base_refs(self):
        lists = []

        tags = self.soup.find_all(name='linkbaseRef')
        for tag in tags:
            dict = {
                'xlink_type': tag.get('xlink:type'),
                'xlink_href': tag.get('xlink:href'),
                'xlink_role': tag.get('xlink:role'),
                'xlink_arcrole': tag.get('xlink:arcrole')
            }

            lists.append(dict)

        self.data = lists

        return self

    def elements(self):
        lists = []

        tags = self.soup.find_all(name='element')
        for tag in tags:
            dict = {
                'id': tag.get('id'),
                'xbrli_balance': tag.get('xbrli:balance'),
                'xbrli_period_type': tag.get('xbrli:periodType'),
                'name': tag.get('name'),
                'nillable': tag.get('nillable'),
                'substitution_group': tag.get('substitutionGroup'),
                'type': tag.get('type'),
                'abstract': tag.get('abstract'),
            }

            lists.append(dict)

        self.data = lists

        return self