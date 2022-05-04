"""A class modeling a newspaper issue in the Daily Princetonian collection.

Newspaper issues in the Daily Princetonian collection are encoded
as METS/ALTO files in a directory, following some conventions:

The METS file is named Princetonian_YYYY-MM-DD_vNN_nNNN_NNNN-METS.xml
The ALTO files are stored in a subdirectory called Princetonian-ALTO;
they are named Princetonian_YYYY-MM-DD_vNN_nNNN_NNNN_ALTONNNN.xml."""

from pathlib import Path
import logging
from sys import stdout
from mets import Mets

_logger = logging.getLogger(__name__)
logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
logging.basicConfig(
    level=logging.DEBUG,
    stream=stdout,
    format=logformat,
    datefmt="%Y-%m-%d %H:%M:%S")


class Issue:
    """Class Issue models a newspaper issue."""

    def __init__(self, resource_path):
        """Resource_path is the path to the subdirectory
        containing the METS and ALTO files."""
        self._path = Path(resource_path)
        self._mets = None
        self._articles = []

    @property
    def mets(self):
        """Instantiate a Mets object if there is none."""
        if not self._mets:
            self._mets = Mets(next(self._path.glob("*METS.xml")))
        return self._mets

    @property
    def date(self):
        return self.mets.date

    @property
    def articles(self):
        """Instantiate a list of articles if there is none."""
        if not self._articles:
            for item in self.mets.articles:
                self._articles.append(Article(item, self.mets))
        return self._articles

    @property
    def jsonl(self):
        return [article.jsonl for article in self.articles]


class Article:
    """A class modeling an article in a METS/ALTO resource."""
    def __init__(self, mets_div, mets):
        self._xml = mets_div
        self.mets = mets

    @property
    def title(self):
        """By convention, the div @LABEL property is the
        article title."""
        return self._xml.get("LABEL")

    @property
    def date(self):
        return self.mets.date

    @property
    def metadata(self):
        metadata = {}
        metadata['title'] = self.title
        metadata['date'] = self.date
        return metadata

    @property
    def areas(self):
        return self._xml.xpath(".//mets:area", namespaces=Mets.ns_map)

    @property
    def text(self):
        """The METS Logical StructMap maps articles to
        sequences of text blocks in ALTO files."""
        areas = self.areas
        content = []
        for area in areas:
            file_id = area.get("FILEID")
            if file_id in self.mets.alto_objects.keys():
                beginning = area.get("BEGIN")
                alto = self.mets.alto_objects[file_id]
                # Handle bad area specs
                if beginning in alto.text_blocks.keys():
                    block = alto.text_blocks[area.get("BEGIN")]
                    content.append(block)

        return ' '.join(content)

    @property
    def jsonl(self):
        data = {}
        data['text'] = self.text
        data['meta'] = self.metadata
        return data
