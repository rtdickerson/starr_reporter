import os 
import sys
import prettyprinter
import csv
import unittest

sys.path.insert(1, "./lib/")

from tea_csv_reader import TEACsvReader

TestFiles = {
    '2018-2019' : "tea_reports/STARR_TEA_TPRS - STAAR FISD 2018-2019.csv",
    "2020-2021" : "tea_reports/STARR_TEA_TPRS - STARR FISD 2020-2021.csv",
    "2021-2022" : "tea_reports/STARR_TEA_TPRS - STARR FISD 2021-2022.csv",
    "2022-2023" : "tea_reports/STARR_TEA_TPRS - STARR FISD 2022-2023.csv",
    "2023-2024" : "tea_reports/STARR_TEA_TPRS - STARR FISD 2023-2024.csv"
}
def getTestFile(TAG):
    return TestFiles[TAG]


class test_TEACsvReader(unittest.TestCase):
    def testOne(self):
        csv_path = getTestFile("2018-2019")
        prettyprinter.pprint(csv_path)
        reader = TEACsvReader(csv_path)
        assert reader is not None
        print ("%d rows" % reader.getRowCount())

    def testCleanString (self):
        csv_path = getTestFile("2018-2019")
        reader = TEACsvReader(csv_path)
        S = reader.safeString("  Hello World  ")
        self.assertEqual(S, "Hello World")
        S = reader.safeString("Grade 3 Reading")
        self.assertEqual(S, "Grade 3 Reading")
        row = reader.get_row(12)
        S = reader.safeString(row[0])
        self.assertEqual(S, "Grade 3 Mathematics", "got '%s'" % S)
    
    def testexploreForKeySections2018(self):
        csv_path = getTestFile("2018-2019")
        reader = TEACsvReader(csv_path)
        SECTS = reader.exploreRowsForKeySections()
        #prettyprinter.pprint(SECTS)
        self.assertTrue(len(SECTS) > 0, "no sections found")
        TDATA = [
            [5, 'Grade 3 Reading'],
            [12, 'Grade 3 Mathematics'],
            [19, 'Grade 4 Reading'],
            [26, 'Grade 4 Mathematics'],
            [33, 'Grade 4 Writing'],
            [40, 'Grade 5 Reading+'],
            [47, 'Grade 5 Mathematics+'],
            [54, 'Grade 5 Science'],
            [61, 'Grade 6 Reading'],
            [68, 'Grade 6 Mathematics'],
            [75, 'Grade 7 Reading'],
            [82, 'Grade 7 Mathematics'],
            [89, 'Grade 7 Writing'],
            [96, 'Grade 8 Reading+'],
            [103, 'Grade 8 Mathematics+'],
            [110, 'Grade 8 Science'],
            [117, 'Grade 8 Social Studies'],
            [124, 'End of Course English I'],
            [131, 'End of Course English II'],
            [138, 'End of Course Algebra I'],
            [145, 'End of Course Biology'],
            [152, 'End of Course U.S. History'],
            [159, 'All Grades All Subjects'],
            [166, 'All Grades ELA/Reading'],
            [173, 'All Grades Mathematics'],
            [180, 'All Grades Writing'],
            [187, 'All Grades Science'],
            [194, 'All Grades Social Studies']
        ]
        self.assertEqual(len(SECTS), len(TDATA), "wrong number of sections")
        for i in range(len(SECTS)):
            self.assertEqual(SECTS[i][0], TDATA[i][0], "wrong row for %s" % TDATA[i][1])
            self.assertEqual(SECTS[i][1], TDATA[i][1], "wrong section name for row %d" % TDATA[i][0])

    def findMissalignedSections(self, SECTS, TDATA):
        inSects = []
        inTdata = []
        for SECT in SECTS:
            FND = False
            for TX in TDATA:
                if SECT[1].startswith(TX[1]):
                    FND = True
                    break
            if not FND:
                inSects.append(SECT[1])
        for TX in TDATA:
            FND = False
            for SECT in SECTS:
                if TX[1].startswith(SECT[1]):
                    FND = True
                    break
            if not FND:
                inTdata.append(TX[1])
        return inSects, inTdata

    def testexploreForKeySections2020(self):
        csv_path = getTestFile("2020-2021")
        reader = TEACsvReader(csv_path)
        SECTS = reader.exploreRowsForKeySections()
        self.assertTrue(len(SECTS) > 0, "no sections found")
        TDATA = [
            [5, 'Grade 3 Reading'],
            [12, 'Grade 3 Mathematics'],
            [19, 'Grade 4 Reading'],
            [26, 'Grade 4 Mathematics'],
            [33, 'Grade 4 Writing'],
            [40, 'Grade 5 Reading+'],
            [47, 'Grade 5 Mathematics+'],
            [54, 'Grade 5 Science'],
            [61, 'Grade 6 Reading'],
            [68, 'Grade 6 Mathematics'],
            [75, 'Grade 7 Reading'],
            [82, 'Grade 7 Mathematics'],
            [89, 'Grade 7 Writing'],
            [96, 'Grade 8 Reading+'],
            [103, 'Grade 8 Mathematics+'],
            [110, 'Grade 8 Science'],
            [117, 'Grade 8 Social Studies'],
            [124, 'End of Course English I'],
            [131, 'End of Course English II'],
            [138, 'End of Course Algebra I'],
            [145, 'End of Course Biology'],
            [152, 'End of Course U.S. History'],
            [159, 'All Grades All Subjects'],
            [166, 'All Grades ELA/Reading'],
            [173, 'All Grades Mathematics'],
            [180, 'All Grades Writing'],
            [187, 'All Grades Science'],
            [194, 'All Grades Social Studies']
        ]
        if len(TDATA) != len(SECTS):
            prettyprinter.pprint(SECTS)
        self.assertEqual(len(SECTS), len(TDATA), "wrong number of sections")
        for i in range(len(SECTS)):
            self.assertEqual(SECTS[i][0], TDATA[i][0], "wrong row for %s" % TDATA[i][1])
            self.assertEqual(SECTS[i][1], TDATA[i][1], "wrong section name for row %d" % TDATA[i][0])


    def testexploreForKeySections2021(self):
        csv_path = getTestFile("2021-2022")
        reader = TEACsvReader(csv_path)
        SECTS = reader.exploreRowsForKeySections()
        self.assertTrue(len(SECTS) > 0, "no sections found")
        TDATA = [
            [5, 'Grade 3 Reading'],
            [12, 'Grade 3 Mathematics'],
            [19, 'Grade 4 Reading'],
            [26, 'Grade 4 Mathematics'],
            [33, 'Grade 5 Reading'],
            [40, 'Grade 5 Mathematics'],
            [47, 'Grade 5 Science'],
            [54, 'Grade 6 Reading'],
            [61, 'Grade 6 Mathematics'],
            [68, 'Grade 7 Reading'],
            [75, 'Grade 7 Mathematics'],
            [82, 'Grade 8 Reading'],
            [89, 'Grade 8 Mathematics'],
            [96, 'Grade 8 Science'],
            [103, 'Grade 8 Social Studies'],
            [110, 'End of Course English I'],
            [117, 'End of Course English II'],
            [124, 'End of Course Algebra I'],
            [131, 'End of Course Biology'],
            [138, 'End of Course U.S. History'],
            [145, 'All Grades All Subjects'],
            [152, 'All Grades ELA/Reading'],
            [159, 'All Grades Mathematics'],
            [166, 'All Grades Science'],
            [173, 'All Grades Social Studies']
        ]
        self.assertEqual(len(SECTS), len(TDATA), "wrong number of sections")
        for i in range(len(SECTS)):
            self.assertEqual(SECTS[i][0], TDATA[i][0], "wrong row for %s" % TDATA[i][1])
            self.assertEqual(SECTS[i][1], TDATA[i][1], "wrong section name for row %d" % TDATA[i][0])

    def testexploreForKeySections2022(self):
        csv_path = getTestFile("2022-2023")
        reader = TEACsvReader(csv_path)
        SECTS = reader.exploreRowsForKeySections()
        prettyprinter.pprint(SECTS)
        self.assertTrue(len(SECTS) > 0, "no sections found")
        TDATA = [
            [5, 'Grade 3 Reading'],
            [12, 'Grade 3 Mathematics'],
            [19, 'Grade 4 Reading'],
            [26, 'Grade 4 Mathematics'],
            [33, 'Grade 5 Reading'],
            [40, 'Grade 5 Mathematics'],
            [47, 'Grade 5 Science'],
            [54, 'Grade 6 Reading'],
            [61, 'Grade 6 Mathematics'],
            [68, 'Grade 7 Reading'],
            [75, 'Grade 7 Mathematics'],
            [82, 'Grade 8 Reading'],
            [89, 'Grade 8 Mathematics'],
            [96, 'Grade 8 Science'],
            [103, 'Grade 8 Social Studies'],
            [110, 'End of Course English I'],
            [117, 'End of Course English II'],
            [124, 'End of Course Algebra I'],
            [131, 'End of Course Biology'],
            [138, 'End of Course U.S. History'],
            [145, 'All Grades All Subjects'],
            [152, 'All Grades ELA/Reading'],
            [159, 'All Grades Mathematics'],
            [166, 'All Grades Science'],
            [173, 'All Grades Social Studies']
        ]
        self.assertEqual(len(SECTS), len(TDATA), "wrong number of sections")
        for i in range(len(SECTS)):
            self.assertEqual(SECTS[i][0], TDATA[i][0], "wrong row for %s" % TDATA[i][1])
            self.assertEqual(SECTS[i][1], TDATA[i][1], "wrong section name for row %d" % TDATA[i][0])

    def testexploreForKeySections2023(self):
        csv_path = getTestFile("2023-2024")
        reader = TEACsvReader(csv_path)
        SECTS = reader.exploreRowsForKeySections()
        prettyprinter.pprint(SECTS)
        self.assertTrue(len(SECTS) > 0, "no sections found")
        TDATA = [
            [5, 'Grade 3 Reading'],
            [12, 'Grade 3 Mathematics'],
            [19, 'Grade 4 Reading'],
            [26, 'Grade 4 Mathematics'],
            [33, 'Grade 5 Reading'],
            [40, 'Grade 5 Mathematics'],
            [47, 'Grade 5 Science'],
            [54, 'Grade 6 Reading'],
            [61, 'Grade 6 Mathematics'],
            [68, 'Grade 7 Reading'],
            [75, 'Grade 7 Mathematics'],
            [82, 'Grade 8 Reading'],
            [89, 'Grade 8 Mathematics'],
            [96, 'Grade 8 Science'],
            [103, 'Grade 8 Social Studies'],
            [110, 'End of Course English I'],
            [117, 'End of Course English II'],
            [124, 'End of Course Algebra I'],
            [131, 'End of Course Biology'],
            [138, 'End of Course U.S. History'],
            [145, 'All Grades All Subjects'],
            [152, 'All Grades ELA/Reading'],
            [159, 'All Grades Mathematics'],
            [166, 'All Grades Science'],
            [173, 'All Grades Social Studies']
        ]
        self.assertEqual(len(SECTS), len(TDATA), "wrong number of sections")
        for i in range(len(SECTS)):
            self.assertEqual(SECTS[i][0], TDATA[i][0], "wrong row for %s" % TDATA[i][1])
            self.assertEqual(SECTS[i][1], TDATA[i][1], "wrong section name for row %d" % TDATA[i][0])
        
    
    def testDiscover2018(self):
        csv_path = getTestFile("2018-2019")
        reader = TEACsvReader(csv_path)
        reader.discoverKeySections("2018-2019")
        self.assertTrue(reader.checkKeySections("2018-2019"), "Failed for 2018-2019")

    def testDiscover2020(self):
        csv_path = getTestFile("2020-2021")
        reader = TEACsvReader(csv_path)
        reader.discoverKeySections("2020-2021")
        self.assertTrue(reader.checkKeySections("2020-2021"), "Failed for 2020-2021")
        
    def testDiscover2021(self):
        csv_path = getTestFile("2021-2022")
        reader = TEACsvReader(csv_path)
        reader.discoverKeySections("2021-2022")
        self.assertTrue(reader.checkKeySections("2021-2022"), "Failed for 2021-2022")

    def testDiscover2022(self):
        csv_path = getTestFile("2022-2023")
        reader = TEACsvReader(csv_path)
        reader.discoverKeySections("2022-2023")
        self.assertTrue(reader.checkKeySections("2022-2023"), "Failed for 2022-2023")

    def testDiscover2023(self):
        csv_path = getTestFile("2023-2024")
        reader = TEACsvReader(csv_path)
        reader.discoverKeySections("2023-2024")
        self.assertTrue(reader.checkKeySections("2023-2024"), "Failed for 2023")
    
    def testGetSection2018(self):
        csv_path = getTestFile("2018-2019")
        reader = TEACsvReader(csv_path)
        reader.discoverKeySections("2018-2019")
        resp = reader.getSection("grade3-reading")
        self.assertIsNotNone(resp, "Grade 3 Reading not found")
        #prettyprinter.pprint(resp)
        TDATA = { 
            'At Approaches Grade Level or Above': {
                '2019': {
                    'TEXAS': '75%',
                    'REGION20': '72%',
                    'FISD': '65%',
                    'African American': '*',
                    'Hispanic': '63%',
                    'White': '68%',
                    'American Indian': '-',
                    'Asian': '*',
                    'Pacific Islander': '-',
                    'Two or More Races': '*',
                    'Special Ed': '17%',
                    'Econ Disadv': '58%',
                    'EB/EL': '66%'
                },
                '2018': {
                    'TEXAS': '77%',
                    'REGION20': '73%',
                    'FISD': '73%',
                    'African American': '67%',
                    'Hispanic': '70%',
                    'White': '77%',
                    'American Indian': '*',
                    'Asian': '*',
                    'Pacific Islander': '-',
                    'Two or More Races': '80%',
                    'Special Ed': '52%',
                    'Econ Disadv': '64%',
                    'EB/EL': '58%'
                }
            }
        }
        self.assertEqual(len(resp.keys()), 3, "wrong number of keys")
        KL = list(TDATA.keys())
        DKL = list(resp.keys())       
        self.assertEqual(DKL[0], KL[0], "wrong toplevel key %s" % DKL[0])
        K = KL[0]
        self.assertEqual(resp[K].keys(), TDATA[K].keys(), "wrong second level keys %s" % resp[K].keys())
        for K2 in resp[K].keys():
            self.assertEqual(resp[K][K2].keys(), TDATA[K][K2].keys(), "wrong third level keys %s" % resp[K][K2].keys())
            for K3 in resp[K][K2].keys():
                self.assertEqual(resp[K][K2][K3], TDATA[K][K2][K3], "wrong value %s" % resp[K][K2][K3])

    def testGetSection2020(self):
        csv_path = getTestFile("2020-2021")
        reader = TEACsvReader(csv_path)
        reader.discoverKeySections("2020-2021")
        resp = reader.getSection("grade3-reading")
        self.assertIsNotNone(resp, "Grade 3 Reading not found")
        #prettyprinter.pprint(resp)
        TDATA = { 
            'At Approaches Grade Level or Above': {
                '2021': {
                    'TEXAS': '67%',
                    'REGION20': '64%',
                    'FISD': '58%',
                    'African American': '*',
                    'Hispanic': '51%',
                    'White': '68%',
                    'American Indian': '*',
                    'Asian': '*',
                    'Pacific Islander': '-',
                    'Two or More Races': '71%',
                    'Special Ed': '16%',
                    'Econ Disadv': '49%',
                    'EB/EL': '27%'
                },
                '2019': {
                    'TEXAS': '75%',
                    'REGION20': '72%',
                    'FISD': '65%',
                    'African American': '*',
                    'Hispanic': '63%',
                    'White': '68%',
                    'American Indian': '-',
                    'Asian': '*',
                    'Pacific Islander': '-',
                    'Two or More Races': '*',
                    'Special Ed': '17%',
                    'Econ Disadv': '58%',
                    'EB/EL': '66%'
                }
            }
        }
        self.assertEqual(len(resp.keys()), 3, "wrong number of keys")
        KL = list(TDATA.keys())
        DKL = list(resp.keys())       
        self.assertEqual(DKL[0], KL[0], "wrong toplevel key %s" % DKL[0])
        K = KL[0]
        self.assertEqual(resp[K].keys(), TDATA[K].keys(), "wrong second level keys %s" % resp[K].keys())
        for K2 in resp[K].keys():
            self.assertEqual(resp[K][K2].keys(), TDATA[K][K2].keys(), "wrong third level keys %s" % resp[K][K2].keys())
            for K3 in resp[K][K2].keys():
                self.assertEqual(resp[K][K2][K3], TDATA[K][K2][K3], "wrong value %s" % resp[K][K2][K3])

    def testGetSection2021(self):
        csv_path = getTestFile("2021-2022")
        reader = TEACsvReader(csv_path)
        reader.discoverKeySections("2021-2022")
        resp = reader.getSection("grade3-reading")
        self.assertIsNotNone(resp, "Grade 3 Reading not found")
        #prettyprinter.pprint(resp)
        TDATA = { 
            'At Approaches Grade Level or Above': {
                '2022': {
                    'TEXAS': '76%',
                    'REGION20': '73%',
                    'FISD': '75%',
                    'African American': '*',
                    'Hispanic': '72%',
                    'White': '79%',
                    'American Indian': '-',
                    'Asian': '-',
                    'Pacific Islander': '-',
                    'Two or More Races': '*',
                    'Special Ed': '50%',
                    'Econ Disadv': '69%',
                    'EB/EL': '57%'
                },
                '2021': {
                    'TEXAS': '67%',
                    'REGION20': '64%',
                    'FISD': '58%',
                    'African American': '*',
                    'Hispanic': '51%',
                    'White': '68%',
                    'American Indian': '*',
                    'Asian': '*',
                    'Pacific Islander': '-',
                    'Two or More Races': '71%',
                    'Special Ed': '16%',
                    'Econ Disadv': '49%',
                    'EB/EL': '27%'
                }
            }
        }
        self.assertEqual(len(resp.keys()), 3, "wrong number of keys")
        KL = list(TDATA.keys())
        DKL = list(resp.keys())       
        self.assertEqual(DKL[0], KL[0], "wrong toplevel key %s" % DKL[0])
        K = KL[0]
        self.assertEqual(resp[K].keys(), TDATA[K].keys(), "wrong second level keys %s" % resp[K].keys())
        for K2 in resp[K].keys():
            self.assertEqual(resp[K][K2].keys(), TDATA[K][K2].keys(), "wrong third level keys %s" % resp[K][K2].keys())
            for K3 in resp[K][K2].keys():
                self.assertEqual(resp[K][K2][K3], TDATA[K][K2][K3], "wrong value %s" % resp[K][K2][K3])

    def testGetSection2022(self):
        csv_path = getTestFile("2022-2023")
        reader = TEACsvReader(csv_path)
        reader.discoverKeySections("2022-2023")
        resp = reader.getSection("grade3-reading")
        self.assertIsNotNone(resp, "Grade 3 Reading not found")
        #prettyprinter.pprint(resp)
        TDATA = { 
            'At Approaches Grade Level or Above': {
                '2023': {
                    'TEXAS': '75%',
                    'REGION20': '73%',
                    'FISD': '67%',
                    'African American': '*',
                    'Hispanic': '64%',
                    'White': '73%',
                    'American Indian': '-',
                    'Asian': '*',
                    'Pacific Islander': '*',
                    'Two or More Races': '86%',
                    'Special Ed': '39%',
                    'Econ Disadv': '58%',
                    'EB/EL': '64%'
                },
                '2022': {
                    'TEXAS': '76%',
                    'REGION20': '73%',
                    'FISD': '75%',
                    'African American': '*',
                    'Hispanic': '72%',
                    'White': '79%',
                    'American Indian': '-',
                    'Asian': '-',
                    'Pacific Islander': '-',
                    'Two or More Races': '*',
                    'Special Ed': '50%',
                    'Econ Disadv': '69%',
                    'EB/EL': '57%'
                }
            }
        }
        self.assertEqual(len(resp.keys()), 3, "wrong number of keys")
        KL = list(TDATA.keys())
        DKL = list(resp.keys())       
        self.assertEqual(DKL[0], KL[0], "wrong toplevel key %s" % DKL[0])
        K = KL[0]
        self.assertEqual(resp[K].keys(), TDATA[K].keys(), "wrong second level keys %s" % resp[K].keys())
        for K2 in resp[K].keys():
            self.assertEqual(resp[K][K2].keys(), TDATA[K][K2].keys(), "wrong third level keys %s" % resp[K][K2].keys())
            for K3 in resp[K][K2].keys():
                self.assertEqual(resp[K][K2][K3], TDATA[K][K2][K3], "wrong value %s" % resp[K][K2][K3])

    def testGetSection2023(self):
        csv_path = getTestFile("2023-2024")
        reader = TEACsvReader(csv_path)
        reader.discoverKeySections("2023-2024")
        resp = reader.getSection("grade3-reading")
        self.assertIsNotNone(resp, "Grade 3 Reading not found")
        #prettyprinter.pprint(resp)
        TDATA = {    
            'At Approaches Grade Level or Above': {
                '2024': {
                    'TEXAS': '72%',
                    'REGION20': '70%',
                    'FISD': '63%',
                    'African American': '*',
                    'Hispanic': '56%',
                    'White': '78%',
                    'American Indian': '*',
                    'Asian': '-',
                    'Pacific Islander': '*',
                    'Two or More Races': '83%',
                    'Special Ed': '39%',
                    'Econ Disadv': '52%',
                    'EB/EL': '35%'
                },
                '2023': {
                    'TEXAS': '75%',
                    'REGION20': '73%',
                    'FISD': '67%',
                    'African American': '*',
                    'Hispanic': '64%',
                    'White': '73%',
                    'American Indian': '-',
                    'Asian': '*',
                    'Pacific Islander': '*',
                    'Two or More Races': '86%',
                    'Special Ed': '39%',
                    'Econ Disadv': '58%',
                    'EB/EL': '64%'
                }
            }
        }
        self.assertEqual(len(resp.keys()), 3, "wrong number of keys")
        KL = list(TDATA.keys())
        DKL = list(resp.keys())       
        self.assertEqual(DKL[0], KL[0], "wrong toplevel key %s" % DKL[0])
        K = KL[0]
        self.assertEqual(resp[K].keys(), TDATA[K].keys(), "wrong second level keys %s" % resp[K].keys())
        for K2 in resp[K].keys():
            self.assertEqual(resp[K][K2].keys(), TDATA[K][K2].keys(), "wrong third level keys %s" % resp[K][K2].keys())
            for K3 in resp[K][K2].keys():
                self.assertEqual(resp[K][K2][K3], TDATA[K][K2][K3], "wrong value %s" % resp[K][K2][K3])
    

    def testRunConverter2018(self):
        csv_path = getTestFile("2018-2019")
        reader = TEACsvReader(csv_path)
        reader.discoverKeySections("2018-2019")
        resp = reader.convertData()
        self.assertIsNotNone(resp, "convertData returned None")
        self.assertEqual(len(resp.keys()), len(reader.key_sections.keys()), "wrong number of keys")

    def testRunConverter2020(self):
        csv_path = getTestFile("2020-2021")
        reader = TEACsvReader(csv_path)
        reader.discoverKeySections("2020-2021")
        resp = reader.convertData()
        self.assertIsNotNone(resp, "convertData returned None")
        self.assertEqual(len(resp.keys()), len(reader.key_sections.keys()), "wrong number of keys")

    def testRunConverter2021(self):
        csv_path = getTestFile("2021-2022")
        reader = TEACsvReader(csv_path)
        reader.discoverKeySections("2021-2022")
        resp = reader.convertData()
        self.assertIsNotNone(resp, "convertData returned None")
        self.assertEqual(len(resp.keys()), len(reader.key_sections.keys()), "wrong number of keys")

    def testRunConverter2022(self):
        csv_path = getTestFile("2022-2023")
        reader = TEACsvReader(csv_path)
        reader.discoverKeySections("2022-2023")
        resp = reader.convertData()
        self.assertIsNotNone(resp, "convertData returned None")
        self.assertEqual(len(resp.keys()), len(reader.key_sections.keys()), "wrong number of keys")

    def testRunConverter2023(self):
        csv_path = getTestFile("2023-2024")
        reader = TEACsvReader(csv_path)
        reader.discoverKeySections("2023-2024")
        resp = reader.convertData()
        self.assertIsNotNone(resp, "convertData returned None")
        self.assertEqual(len(resp.keys()), len(reader.key_sections.keys()), "wrong number of keys")

    def testGetScore(self):
        csv_path = getTestFile("2023-2024")
        reader = TEACsvReader(csv_path)
        F = reader.getScore("98%")
        self.assertEqual(F, 98.0, "Did not parse correctly %5.3f" % F)
        F = reader.getScore("")
        self.assertEqual(F, -1.0, "Did not parse correctly %5.3f" % F)
        F = reader.getScore("*")
        self.assertEqual(F, -1.0, "Did not parse correctly %5.3f" % F)
        
    