from recommonmark.parser import CommonMarkParser
# from CommonMark import Parser
from .pykramdown import ParserWithTables
from docutils import nodes  # parsers
import re

reFrontMaters = re.compile(
    r"(?:^-{3}\n)((?:\w+:\s*[^\n]+\n)+)(?:-{3}\n)"
    )
reFMKey = re.compile(
            r"(?P<key>(?:\w)+):\s*(?P<value>[^\n]+)\n",
            re.MULTILINE
            )
reFMid = re.compile(r"([^./]+)(?=.html)", re.MULTILINE)
# reFMid = re.compile(r"([^./]+\.html)", re.MULTILINE)
reAldTypeID = re.compile(r"#([A-Za-z][\w:-]*)")

reUrl = re.compile(r"^\w+:/")
reBase = re.compile(r"((?:\w|[-])+)\.html")
reDetail = re.compile(r"#((?:\w|[-])+)")


class KramdownParser(CommonMarkParser):

    def parse_front(self, params):

        prop = {m.group('key'): m.group('value')
                for m in re.finditer(reFMKey, params)}
        title = prop.get('title')
        permalink = prop.get('permalink')

        # att = {}
        if title:
            # att['title']  = title
            # att['names'] = title.lower()
            # att['ids'] = att['names'].replace(' ', '-')

            title_node = nodes.title(text=title)
            title_node.line = 0

            new_section = nodes.section()
            new_section.line = 0
            new_section.append(title_node)

            self.add_section(new_section, 1)
            name = nodes.fully_normalize_name(title)
            if permalink:
                match = re.search(reFMid, permalink)
                if match:
                    ids = match.group(0)
                    new_section['ids'].append(ids)
                    new_section['names'].append(ids)
            new_section['names'].append(name)
            self.document.note_implicit_target(new_section, new_section)
            self.current_node = new_section

    def parse(self, inputstring, document):
        self.document = document
        self.current_node = document
        match = re.match(reFrontMaters, inputstring)

        if match:
            inputstring = inputstring[match.end()+1:]

        self.setup_parse(inputstring, document)
        self.setup_sections()
        if match:
            self.parse_front(match.group(1))
        parser = ParserWithTables()
        ast = parser.parse(inputstring + '\n')
        self.convert_ast(ast)
        self.finish_parse()

    def visit_table_block(self, mdnode):
        kwargs = {}
        kwargs['language'] = 'text'
        text = "table_block stub\n"+''.join(mdnode.literal)
        if text.endswith('\n'):
            text = text[:-1]
        node = nodes.literal_block(text, text, **kwargs)
        self.current_node.append(node)

    def visit_ald_inline(self, mdnode):
        return
        print(mdnode, mdnode.prv, mdnode.nxt, mdnode.parent)
        kwargs = {}
        kwargs['language'] = 'text'
        text = "ald_block stub\n"+''.join(mdnode.literal)
        if text.endswith('\n'):
            text = text[:-1]
        node = nodes.literal_block(text, text, **kwargs)
        self.current_node.append(node)

    def visit_liqid_inline(self, mdnode):
        kwargs = {}
        kwargs['language'] = 'text'
        text = "liqid template: like \".. altair-object-table::\" \n"+''.join(mdnode.literal)
        if text.endswith('\n'):
            text = text[:-1]
        node = nodes.literal_block(text, text, **kwargs)
        node['classes'].append('red')
        self.current_node.append(node)

    def depart_heading(self, mdnode):
        """Finish establishing section

        Wrap up title node, but stick in the section node. Add the section names
        based on all the text nodes added to the title.
        """
        assert isinstance(self.current_node, nodes.title)
        # The title node has a tree of text nodes, use the whole thing to
        # determine the section id and names
        text = self.current_node.astext()
        if self.translate_section_name:
            text = self.translate_section_name(text)
        name = nodes.fully_normalize_name(text)
        section = self.current_node.parent
        section['names'].append(name)

        if mdnode and mdnode.prv and mdnode.prv.last_child and\
                mdnode.prv.last_child.t == 'ald_inline':
                match = reAldTypeID.search(mdnode.prv.last_child.literal)
                if match:
                    section['names'].append(match.group(1))
                    section['ids'] = [match.group(1)]

        self.document.note_implicit_target(section, section)
        self.current_node = section
    
    def visit_link(self, mdnode):
        if not reUrl.search(mdnode.destination):
            m = reDetail.search(mdnode.destination)
            if m:
                mdnode.destination = m.group(1)
            else:
                m = reBase.search(mdnode.destination)
                if m:
                    mdnode.destination = m.group(1)

        print("vl:", mdnode.destination)
        return super().visit_link(mdnode)
