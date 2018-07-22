import importlib
import warnings
import json

import jsonschema

from docutils.parsers.rst import Directive
from docutils.statemachine import ViewList
from docutils import nodes, utils
from recommonmark.parser import CommonMarkParser
from sphinx.util.nodes import nested_parse_with_titles
from sphinx import addnodes
import re




class AltairObjectTableDirective(Directive):
    """
    Directive for building a table of attribute descriptions.

    Usage:

    .. altair-object-table:: altair.MarkConfig

    """
    has_content = False
    required_arguments = 1

    def type_description(self, schema):
        """Return a concise type description for the given schema"""
        if schema == {}:
            return 'any'
        elif "$ref" in schema:
            return ":class:`{0}`".format(schema['$ref'].split('/')[-1])
        elif 'enum' in schema:
            return "[{0}]".format(', '.join(repr(s) for s in schema['enum']))
        elif 'type' in schema:
            if isinstance(schema['type'], list):
                return '[{0}]'.format(', '.join(schema['type']))
            elif schema['type'] == 'array':
                return 'array({0})'.format(self.type_description(schema.get('items', {})))
            elif schema['type'] == 'object':
                return 'dict'
            else:
                return schema['type']
        elif 'anyOf' in schema:
            return "anyOf({0})".format(', '.join(self.type_description(s)
                                                for s in schema['anyOf']))
        else:
            warnings.warn('cannot infer type for schema with keys {0}'
                        ''.format(schema.keys()))
            return '--'


    def iter_properties(self, cls):
        """Iterate over (property, type, description)"""
        schema = cls.resolve_references(cls._schema)
        properties = schema.get('properties', {})
        mdparser = CommonMarkParser()
        for prop, propschema in properties.items():
            doc = utils.new_document("md_doc")
            mdparser.parse(propschema.get('description', ' '), doc)
            descr = nodes.paragraph()
            descr.document = self.state.document
            nested_parse_with_titles(self.state, nodes.paragraph( text =self.type_description(propschema)), descr)
            
            yield ( [nodes.paragraph(text = prop)],
                   # [nodes.paragraph(text = self.type_description(propschema))], # ?class
                    descr.children,
                    doc.children)


    def build_rst_table(self, rows, titles, widths):
        """Build an table from a table of entries (i.e. list of lists)"""
        ncols = len(titles)
        assert all(len(row) == ncols for row in rows)
        assert len(titles) == ncols and len(widths) == ncols

        tgroup =  nodes.tgroup(cols = ncols)
        for width in widths:
            tgroup += nodes.colspec(colwidth=width)
        header = nodes.row()
        for title in titles:
            header += nodes.entry('',nodes.paragraph(text = title))
        tgroup += nodes.thead('', header)

        tbody = nodes.tbody()
        for row in rows:
            line = nodes.row()
            for item in row:
                line += nodes.entry('',*item)
            tbody+=line
        tgroup += tbody
    
        return nodes.table('', tgroup)

    def construct_schema_table(self, cls):
        """Construct an RST table describing the properties within a schema."""
        props = list(self.iter_properties(cls))
        # names, types, defs = zip(*props)
        # defs = [defn.replace('\n', ' ') for defn in defs]
        # props = list(zip(names, types, defs))
        return self.build_rst_table(props, ["Property", "Type", "Description"],[10,20,50])

    def run(self):
        objectname = self.arguments[0]
        modname, classname = objectname.rsplit('.', 1)
        module = importlib.import_module(modname)
        cls = getattr(module, classname)

        # create the table from the object
        table = self.construct_schema_table(cls)

        # descr = nodes.paragraph()
        # descr.document = self.state.document
        # nested_parse_with_titles(self.state, table, descr)

        return [table]
        

def prepare_table_header(titles, widths):
    """Build docutil empty table """
    ncols = len(titles)
    assert len(widths) == ncols

    tgroup = nodes.tgroup(cols=ncols)
    for width in widths:
        tgroup += nodes.colspec(colwidth=width)
    header = nodes.row()
    for title in titles:
        header += nodes.entry('', nodes.paragraph(text=title))
    tgroup += nodes.thead('', header)

    tbody = nodes.tbody()
    tgroup += tbody

    return nodes.table('', tgroup), tbody


def type_description(schema):
    """Return a concise type description for the given schema"""
    if schema == {}:
        return 'any'
    elif "$ref" in schema:
        return ":class:`{0}`".format(schema['$ref'].split('/')[-1])
    elif 'enum' in schema:
        return "[{0}]".format(', '.join(repr(s) for s in schema['enum']))
    elif 'type' in schema:
        if isinstance(schema['type'], list):
            return '[{0}]'.format(', '.join(schema['type']))
        elif schema['type'] == 'array':
            return 'array({0})'.format(type_description(schema.get('items', {})))
        elif schema['type'] == 'object':
            return 'dict'
        else:
            return schema['type']
    elif 'anyOf' in schema:
        return "anyOf({0})".format(', '.join(type_description(s)
                                            for s in schema['anyOf']))
    else:
        warnings.warn('cannot infer type for schema with keys {0}'
                    ''.format(schema.keys()))
        return '--'

reClassDef = re.compile (r":class:`([^`]+)`")


def build_row(item):
    """Return nodes.row with property description"""

    prop, propschema, required = item
    row = nodes.row()

    # Property 
    row += nodes.entry('', nodes.paragraph(text=prop))

    # Type
    str_type = type_description(propschema) 
    par_type = nodes.paragraph()

    is_text = True
    for part in reClassDef.split(str_type):
        if part:
            if is_text:
                par_type += nodes.Text(part)
            else:
                par_type += addnodes.pending_xref(
                    reftarget=part,
                    reftype="class",
                    refdomain=None,  # py:class="None" py:module="altair" refdoc="user_guide/marks"
                    refexplicit=False,
                    refwarn=False
                )
                par_type += nodes.literal(text = part,classes="xref py py-class")      
        is_text = not is_text

    row += nodes.entry('', par_type)

    # Description
    md_parser = CommonMarkParser()
    str_descr = "***Required.*** " if required else ""
    str_descr += propschema.get('description', ' ')
    doc_descr = utils.new_document("schema_description")   
    md_parser.parse(str_descr, doc_descr)   
    
    row += nodes.entry('', *doc_descr.children)

    return row


def build_schema_tabel(items):
    """Return schema table of items (iterator of prop, schema.item, requred)"""
    table, tbody = prepare_table_header(
        ["Property", "Type", "Description"],
        [10, 20, 50]
    )
    for item in items:
        tbody += build_row(item)

    return table

  
def select_items_from_schema(schema, props=None):
    """Return iterator  (prop, schema.item, requred) on prop, return all in None"""

    properties = schema.get('properties', {})
    required = schema.get('required', [])
    print(required)
    if not props:
        for prop, item in properties.items():
            yield prop, item, prop in required
    else:
        for prop in props:
            try:
                yield prop, properties[prop], prop in required
            except KeyError:
                warnings.warn("Can't find property:", prop)
  

def prepare_schema_tabel(schema, props=None):

    items = select_items_from_schema(schema, props)
    return build_schema_tabel(items)


def setup(app):
    app.add_directive('altair-object-table', AltairObjectTableDirective)
