"""A class interface to a METS file in the Daily Princetonian collection."""


from pathlib import Path
from lxml import etree
from alto import Alto


class Mets:
    ns_map = {'mets': 'http://www.loc.gov/METS/',
              'mods': 'http://www.loc.gov/mods/v3',
              'xlink': 'http://www.w3.org/1999/xlink'}

    def __init__(self, path):
        self._path = Path(path)
        self._xml = None
        self._alto_objects = {}
        

    @property
    def xml(self):
        if not self._xml:
            with open(self._path, 'r', encoding='utf-8') as f:
                self._xml = etree.parse(f)
        return self._xml

    @property
    def articles(self):
        return self.xml.xpath(
            "//mets:structMap[@TYPE='LOGICAL']//mets:div[@TYPE='ARTICLE']",
                              namespaces=self.ns_map)

    @property
    def alto_objects(self):
        if not self._alto_objects:
            file_elements = self.xml.xpath(
                "//mets:fileGrp[@ID='ALTOGRP']/mets:file",
                namespaces=self.ns_map)
            for e in file_elements:
                key = e.get("ID")
                href = e.xpath("mets:FLocat/@xlink:href",
                               namespaces=self.ns_map)[0]
                _,subdir,fname = Path(href).parts
                alto_path = self._path.parent / subdir / fname
                self._alto_objects[key] = Alto(alto_path)
        return self._alto_objects
            

    def alto_path(self, fileid):
        pathfn = etree.XPath("//mets:file[@ID=$id]/mets:FLocat/@xlink:href",
                             namespaces=self.ns_map)
        return pathfn(self.xml, id=fileid)

mets_path = "/Users/cwulfman/repos/github/pulibrary/corpus-generator/tests/data/06_01/Princetonian_1968-05-06_v92_n061_0001-METS.xml"

with open(mets_path, 'r', encoding='utf-8') as f:
    mets = etree.parse(f)

# try some xpath.
ns_map = {'mets': 'http://www.loc.gov/METS/',
          'mods': 'http://www.loc.gov/mods/v3',
          'xlinka': 'http://www.w3.org/TR/xlink',
          'xlink': 'http://www.w3.org/1999/xlink'}


logical_structMap = mets.xpath("//mets:structMap[@TYPE='LOGICAL']",
                               namespaces=ns_map)[0]
# print(logical_structMap.getparent())

# try compiling xpaths
fn = etree.XPath("//mets:structMap[@TYPE=$type]", namespaces=ns_map)
print(len(fn(mets, type="LOGICAL")))

m = Mets(mets_path)
