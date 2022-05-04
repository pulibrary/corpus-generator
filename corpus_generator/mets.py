"""A class interface to a METS file in the Daily Princetonian collection."""


from pathlib import Path
from lxml import etree
from alto import Alto


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
    def date(self):
        """Returns publication date.

        Several encoding profiles were used in the DailyPrincetonian
        project.  In one (the one used most), there is a single MODS
        record for the entire issue, in a single mets:dmdSec, and the
        date is at this xpath:
        
        //mods:mods/mods:part[@type='issue']/mods:date

        In the second, less-used profile, there are multiple dmdSecs,
        and the issue date can be found here:

        //mets:dmdSec[@ID='MODSMD_ISSUE1']//mods:originInfo/mods:dateIssued

        """
        the_date = None
        path = self.xml.xpath("//mods:date", namespaces=self.ns_map)
        if not path:
            path = self.xml.xpath("//mets:dmdSec[@ID='MODSMD_ISSUE1']//mods:originInfo/mods:dateIssued",
                                  namespaces=self.ns_map)
        if path:
            the_date = path[0].text
        return the_date

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
                # The dataset uses two namespaces for xlink:
                # http://www.w3.org/1999/xlink and http://www.w3.org/TR/xlink.
                # Try both.
                try:
                    href = ele.xpath("mets:FLocat/@xlink:href",
                                     namespaces=self.ns_map)[0]
                except:
                    try:
                        ns_map = {'mets': 'http://www.loc.gov/METS/',
                                  'xlink': 'http://www.w3.org/TR/xlink'}
                        href = ele.xpath("mets:FLocat/@xlink:href",
                                         namespaces=ns_map)[0]
                    except IndexError:
                        raise IndexError("href not found")
                    

                _, subdir, fname = Path(href).parts
                alto_path = self._path.parent / subdir / fname
                self._alto_objects[key] = Alto(alto_path)
        return self._alto_objects

    def alto_path(self, fileid):
        """No longer needed?"""
        pathfn = etree.XPath("//mets:file[@ID=$id]/mets:FLocat/@xlink:href",
                             namespaces=self.ns_map)
        return pathfn(self.xml, id=fileid)
