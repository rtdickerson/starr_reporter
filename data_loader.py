import os
import sys 
import prettyprinter
import csv
import numpy as np

#from sqlitewrapper import SqliteWrapper
sys.path.insert(1, "./lib/")

from tea_compiler import TEADataCompiler

COMP = TEADataCompiler()
for SEC in COMP.reader.key_sections.keys():
    CSV = COMP.collectionToCsv(SEC)
    print ("%s\n\n" % CSV)
    