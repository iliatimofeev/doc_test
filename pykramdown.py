# from collections import defaultdict

import CommonMark
import CommonMark.blocks
import CommonMark.node
from CommonMark.inlines import InlineParser
from CommonMark.node import Node

# Mokey-patch the reMaybeSpecial regex to add our table symbol |.
# This regex is apparently just an optimization so this should not
# affect CommonMark parser instances that do not recognize tables.
import re
CommonMark.blocks.reMaybeSpecial = re.compile(r'^[#`~*+_=<>0-9-|]')
reTableRow = re.compile(r"([^\n]*(?<!\\)(\|))+([^\n]*)")
ALD_ANY_CHARS = r"\\\}|[^\}]"  # /

IAL_BLOCK = r"\{:(?!:|\/)(" + ALD_ANY_CHARS + r"+)\}"

LIQID_BLOCK = r"\{%(" + ALD_ANY_CHARS + r"+)%\}"


reAldBlock = re.compile(IAL_BLOCK, re.M)
reLiqidBlock = re.compile(LIQID_BLOCK, re.M)

# Define a new BlockStarts class that implements a table method
# to detect and parse table starts, modeled after the blockquote.


class BlockStarts(CommonMark.blocks.BlockStarts):
    def __init__(self):
        self.METHODS = ["table_block", "ald_block"] + self.METHODS

    @staticmethod
    def table_block(parser, container=None):
        ln = parser.current_line
        # match = re.search(reTableRow, ln[parser.next_nonspace:])
        if parser.tip.t != 'paragraph' and \
                           not parser.blank and\
                           re.search(reTableRow, ln[parser.next_nonspace:]):
            # indented code
            # parser.advance_offset(CODE_INDENT, True)
            parser.close_unmatched_blocks()
            parser.add_child('table_block', parser.offset)
            return 2

        return 0

    @staticmethod    
    def ald_block(parser, container=None):
        ln = parser.current_line
        # match = re.search(reTableRow, ln[parser.next_nonspace:])
        if parser.tip.t != 'paragraph' and \
                           not parser.blank and\
                           reAldBlock.search(ln[parser.next_nonspace:]):
            # indented code
            # parser.advance_offset(CODE_INDENT, True)
            parser.close_unmatched_blocks()
            parser.add_child('ald_block', parser.offset)
            return 2

        return 0


class AldBlock(CommonMark.blocks.Block):
    accepts_lines = True

    @staticmethod
    def continue_(parser=None, container=None):
        ln = parser.current_line
        match = reAldBlock.search(ln[parser.next_nonspace:])
        if not match:
            # parser.finalize(container, parser.line_number)
            return 1
        else:
            return 0

    @staticmethod
    def finalize(parser=None, block=None):
        if block.string_content:
            text = re.sub(r'(\n *)+$', '\n', block.string_content)
            text = re.sub(r'(\n)$', '', text)
            block.literal = text
            block.string_content = None
            # parser.close_unmatched_blocks()
        
    @staticmethod
    def can_contain(t):
        return False


CommonMark.blocks.AldBlock = AldBlock


class TableBlock(CommonMark.blocks.Block):
    accepts_lines = True

    @staticmethod
    def continue_(parser=None, container=None):
        ln = parser.current_line
        match = re.search(reTableRow, ln[parser.next_nonspace:])
        if not match:
            parser.finalize(container, parser.line_number-1)
            return 2
        else:
            return 0

    @staticmethod
    def finalize(parser=None, block=None):

        block.literal = re.sub(r'(\n *)+$', '\n', block.string_content)
        block.string_content = None

    @staticmethod
    def can_contain(t):
        return False


CommonMark.blocks.TableBlock = TableBlock


class InlineParserWithAld(InlineParser):

    def parseAltTag(self, block):
        """Attempt to parse a raw ALD tag."""
        m = self.match(reAldBlock)
        if m is None:
            return False
        else:
            node = Node('ald_inline', None)
            node.literal = m
            block.append_child(node)
            return True

    def parseLiqidTag(self, block):
        """Attempt to parse a raw Liqid tag."""
        m = self.match(reLiqidBlock)
        if m is None:
            return False
        else:
            node = Node('liqid_inline', None)
            node.literal = m
            block.append_child(node)
            return True
            
    def parseInline(self, block):
        """
        Parse the next inline element in subject, advancing subject
        position.

        On success, add the result to block's children and return True.
        On failure, return False.
        """
        res = False
        c = self.peek()
        if c == '{':
            res = self.parseAltTag(block) or self.parseLiqidTag(block)
        if not res:
            res = super().parseInline(block)
        return res


# Create a new parser sub-class that adds the new block-start
# for tables.
class ParserWithTables(CommonMark.Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.block_starts = BlockStarts()
        self.inline_parser = InlineParserWithAld()
