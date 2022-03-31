"""A class interface to an ALTO file in the Daily Princetonian collection.

NB: the ALTO files in the collection are not properly name-spaced; the
elements are not in the alto namespace.
"""

from lxml import etree


class Alto:
    def __init__(self, path):
        self._path = path
        self._xml = None
        self._text_blocks = {}

    @property
    def xml(self):
        if not self._xml:
            with open(self._path, 'r', encoding='utf-8') as f:
                self._xml = etree.parse(f)
        return self._xml

    @property
    def file_id(self):
        stem = self._path.stem
        return stem.split('_')[-1]

    @property
    def text_blocks(self):
        if not self._text_blocks:
            for block in self.xml.findall(".//TextBlock"):
                self._text_blocks[block.get("ID")] = text_lines(block)
        return self._text_blocks


def text_lines(block):
    lines = []
    for line in block.findall("TextLine"):
        lines.append(text_line(line))
    return " ".join(lines)


def text_line(line_element):
    line = ""
    for child in line_element:
        tag = child.tag
        if tag == 'SP':
            line += ' '
        elif tag == 'HYP':
            pass
        elif tag == 'String':
            if (child.get('SUBS_TYPE') == "HypPart1"):
                line += child.get("SUBS_CONTENT")
            elif (child.get('SUBS_TYPE') == "HypPart2"):
                pass
            else:
                line += child.get("CONTENT")
    return line
