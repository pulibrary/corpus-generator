"""A class interface to a METS file in the Daily Princetonian collection."""


from pathlib import Path
from lxml import etree
from .alto import Alto


class Mets:
    """Implements an interface to a METS XML element."""
    ns_map = {'mets': 'http://www.loc.gov/METS/',
              'mods': 'http://www.loc.gov/mods/v3',
              'xlink': 'http://www.w3.org/1999/xlink'}

    def __init__(self, path):
        self._path = Path(path)
        self._xml = None
        self._alto_objects = {}

    @property
    def xml(self):
        """Returns etree of the METS document."""
        if not self._xml:
            with open(self._path, 'r', encoding='utf-8') as path:
                self._xml = etree.parse(path)
        return self._xml

    @property
    def articles(self):
        """Returns article divs from the METS document."""
        return self.xml.xpath(
            "//mets:structMap[@TYPE='LOGICAL']//mets:div[@TYPE='ARTICLE']",
            namespaces=self.ns_map)

    @property
    def alto_objects(self):
        """Returns the alto objects associated with this METS file,
        constructing a hash of them if necessary.

        The METS file encodes the location of the ALTO files
        as mal-formed file URLs. These file URLs have to be munged
        to get a proper path to the file on disk."""
        if not self._alto_objects:
            file_elements = self.xml.xpath(
                "//mets:fileGrp[@ID='ALTOGRP']/mets:file",
                namespaces=self.ns_map)
            for ele in file_elements:
                key = ele.get("ID")
                href = ele.xpath("mets:FLocat/@xlink:href",
                                 namespaces=self.ns_map)[0]
                _, subdir, fname = Path(href).parts
                alto_path = self._path.parent / subdir / fname
                self._alto_objects[key] = Alto(alto_path)
        return self._alto_objects

    def alto_path(self, fileid):
        """No longer needed?"""
        pathfn = etree.XPath("//mets:file[@ID=$id]/mets:FLocat/@xlink:href",
                             namespaces=self.ns_map)
        return pathfn(self.xml, id=fileid)
