import os
from corpus_generator.mets import Mets


mets_path = f"{os.path.dirname(__file__)}/data/06_01/Princetonian_1968-05-06_v92_n061_0001-METS.xml"

def test_date():
    subject = Mets(mets_path)
    assert subject.date == "1968-05-06"
