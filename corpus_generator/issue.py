"""A class modeling a newspaper issue in the Daily Princetonian collection."""

from pathlib import Path
from  mets import Mets
from  alto import Alto


class Issue:
    def __init__(self, path):
        self._path = Path(path)
        self._mets = None
        self._articles = []

    @property
    def mets(self):
        if not self._mets:
            self._mets = Mets(next(self._path.glob("*METS.xml")))
        return self._mets

    @property
    def articles(self):
        if not self._articles:
            for item in self.mets.articles:
                self._articles.append(Article(item, self.mets))
        return self._articles

class Article:
    def __init__(self, mets_div, mets):
        self._xml = mets_div
        self.mets = mets

    @property
    def title(self):
        return self._xml.get("LABEL")

    @property
    def text(self):
        areas = self._xml.xpath(".//mets:area", namespaces = Mets.ns_map)
        content = []
        for area in areas:
            file_id = area.get("FILEID")
            alto = self.mets.alto_objects[file_id]
            block = alto.text_blocks[area.get("BEGIN")]
            # content.append(' '.join(list(block.values())))
            content.append(block)
        return content

            
issue_path = "/Users/cwulfman/repos/github/pulibrary/corpus-generator/tests/data/06_01"

issue = Issue(issue_path)
article = issue.articles[1]
    
