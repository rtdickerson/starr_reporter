import os 
import sys
import prettyprinter
import csv
import unittest
from json import dumps as json_dumps

sys.path.insert(1, "./lib/")

from tea_csv_reader import TEACsvReader
from tea_compiler import TEADataCompiler

TestFiles = {
    '2018-2019' : "tea_reports/STARR_TEA_TPRS - STAAR FISD 2018-2019.csv",
    "2020-2021" : "tea_reports/STARR_TEA_TPRS - STARR FISD 2020-2021.csv",
    "2021-2022" : "tea_reports/STARR_TEA_TPRS - STARR FISD 2021-2022.csv",
    "2022-2023" : "tea_reports/STARR_TEA_TPRS - STARR FISD 2022-2023.csv",
    "2023-2024" : "tea_reports/STARR_TEA_TPRS - STARR FISD 2023-2024.csv"
}
def getTestFile(TAG):
    return TestFiles[TAG]

class test_TEACompiler(unittest.TestCase):
    
    def testResultForYearSection(self):
        COMP = TEADataCompiler()
        FH = open("dump.json", "w")
        FH.write(json_dumps(COMP.LOADED, indent=4))
        FH.close()
        self.assertIsNotNone(COMP, "constructor failed to load the data")
        sdata = COMP.getResultForYearSection("2018-2019", "grade3-reading")
        self.assertIsNotNone(sdata, "null returned!")
        prettyprinter.pprint(sdata)

    def testResultForYearSection2020(self):
        COMP = TEADataCompiler()
        self.assertIsNotNone(COMP, "constructor failed to load the data")
        sdata = COMP.getResultForYearSection("2020-2021", "grade3-reading")
        self.assertIsNotNone(sdata, "null returned!")
        prettyprinter.pprint(sdata)

    def testResultForYearSection2021(self):
        COMP = TEADataCompiler()
        self.assertIsNotNone(COMP, "constructor failed to load the data")
        sdata = COMP.getResultForYearSection("2021-2022", "grade4-writing")
        self.assertIsNotNone(sdata, "null returned!")
        prettyprinter.pprint(sdata)
        
    def testTransformYearSection2018(self):
        COMP = TEADataCompiler()
        self.assertIsNotNone(COMP, "constructor failed to load the data")
        sdata = COMP.transformYearSection("2018-2019", "grade3-reading")
        self.assertIsNotNone(sdata, "null returned!")
        prettyprinter.pprint(sdata)

    def testTransformYearSection2018B(self):
        COMP = TEADataCompiler()
        self.assertIsNotNone(COMP, "constructor failed to load the data")
        sdata = COMP.transformYearSection("2018-2019", "grade4-writing")
        self.assertIsNotNone(sdata, "null returned!")
        prettyprinter.pprint(sdata)

    def testTransformYearSection2020(self):
        COMP = TEADataCompiler()
        self.assertIsNotNone(COMP, "constructor failed to load the data")
        sdata = COMP.transformYearSection("2018-2019", "grade3-reading")
        self.assertIsNotNone(sdata, "null returned!")
        prettyprinter.pprint(sdata)

    def testTransformYearSection2021(self):
        COMP = TEADataCompiler()
        self.assertIsNotNone(COMP, "constructor failed to load the data")
        sdata = COMP.transformYearSection("2018-2019", "grade4-writing")
        self.assertIsNotNone(sdata, "null returned!")
        prettyprinter.pprint(sdata)

    def testTransformYearSection2022(self):
        COMP = TEADataCompiler()
        self.assertIsNotNone(COMP, "constructor failed to load the data")
        sdata = COMP.transformYearSection("2022-2023", "grade4-writing")
        self.assertIsNone(sdata, "not null returned for empty year!")
        prettyprinter.pprint(sdata)

    def testCollectSectionAcrossTimeReading(self):
        COMP = TEADataCompiler()
        self.assertIsNotNone(COMP, "constructor failed to load the data")
        sdata = COMP.collectSectionAcrossTime("grade4-reading")
        self.assertIsNotNone(sdata, "null returned!")
        prettyprinter.pprint(sdata)

    def testCollectSectionAcrossTimeWriting(self):
        COMP = TEADataCompiler()
        self.assertIsNotNone(COMP, "constructor failed to load the data")
        sdata = COMP.collectSectionAcrossTime("grade4-writing")
        self.assertIsNotNone(sdata, "null returned!")
        prettyprinter.pprint(sdata)

    def testCollectionToCsvReading(self):
        COMP = TEADataCompiler()
        self.assertIsNotNone(COMP, "constructor failed to load the data")
        sdata = COMP.collectionToCsv("grade3-reading")
        self.assertIsNotNone(sdata, "null returned!")
        prettyprinter.pprint(sdata)

    def testCollectionToCsvWriting(self):
        COMP = TEADataCompiler()
        self.assertIsNotNone(COMP, "constructor failed to load the data")
        sdata = COMP.collectionToCsv("grade4-writing")
        self.assertIsNotNone(sdata, "null returned!")
        prettyprinter.pprint(sdata)

    def testGetScore(self):
        csv_path = getTestFile("2023-2024")
        reader = TEACsvReader(csv_path)
        F = reader.getScore("98%")
        self.assertEqual(F, 98.0, "Did not parse correctly %5.3f" % F)
        F = reader.getScore("")
        self.assertEqual(F, -1.0, "Did not parse correctly %5.3f" % F)
        F = reader.getScore("*")
        self.assertEqual(F, -1.0, "Did not parse correctly %5.3f" % F)
