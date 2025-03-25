import os
import sys
import prettyprinter
import csv
import numpy as np
import re  # Add this import at the top of the file


class TEACsvReader:
    def __init__(self, csv_path):
        self.key_columns = {
            "TEXAS" : 2,
            "REGION20" : 3,
            "FISD" : 4,
            "African American" : 5,
            "Hispanic" : 6, 
            "White" : 7,
            "American Indian" : 8,
            "Asian" : 9,
            "Pacific Islander" : 10,
            "Two or More Races" : 11,
            "Special Ed" : 12,
            "Econ Disadv" : 13,
            "EB/EL" : 14,
        }
        self.key_sections = {
            "grade3-reading" : { "tag" : "Grade 3 Reading", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"] },
            "grade3-math" : { "tag" : "Grade 3 Mathematics", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "grade4-reading" : { "tag" : "Grade 4 Reading", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "grade4-math" : { "tag" : "Grade 4 Mathematics", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            # not in 2020-2021 STARR report
            "grade4-writing" : { "tag" : "Grade 4 Writing", "row" : -1, "years" : ["2018-2019","2020-2021"]},
            "grade5-reading" : { "tag" : "Grade 5 Reading", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "grade5-math" : { "tag" : "Grade 5 Mathematics", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "grade5-science" : { "tag" : "Grade 5 Science", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "grade6-reading" : { "tag" : "Grade 6 Reading", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "grade6-math" : { "tag" : "Grade 6 Mathematics", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "grade7-reading" : { "tag" :  "Grade 7 Reading", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "grade7-math" : { "tag" :  "Grade 7 Mathematics", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "grade7-writing" : { "tag" : "Grade 7 Writing", "row" : -1, "years" : ["2018-2019","2020-2021"]},
            "grade8-reading" : { "tag" : "Grade 8 Reading", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "grade8-math" : { "tag" : "Grade 8 Mathematics", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "grade8-science" : { "tag" : "Grade 8 Science", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "grade8-social-studies" : { "tag" : "Grade 8 Social Studies", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "eoc-english-1" : { "tag" : "End of Course English I", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "eoc-english-2" : { "tag" : "End of Course English II", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "eoc-algebra-1" : { "tag" : "End of Course Algebra I", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "eoc-biology" : { "tag" : "End of Course Biology", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "eoc-us-history" : { "tag" : "End of Course U.S. History", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "all-grades-all-subjects" : { "tag" : "All Grades All Subjects", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "all-grades-ela-reading" : { "tag" : "All Grades ELA/Reading", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "all-grades-math" : { "tag" : "All Grades Mathematics", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "all-grades-writing" : { "tag" : "All Grades Writing", "row" : -1, "years" : ["2018-2019","2020-2021"]},
            "all-grades-science" : { "tag" : "All Grades Science", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
            "all-grades-social-studies" : { "tag" : "All Grades Social Studies", "row" : -1, "years" : ["2018-2019","2020-2021","2021-2022","2022-2023","2023-2024"]},
        }
        self.sections = {
            "At Approaches Grade Level or Above" : "approaches",
            "At Meets Grade Level or Above" : "meets",
            "At Masters Grade Level or Above" : "masters",
        }
        self.csv_path = csv_path
        self.csv_file = open(csv_path, 'r')
        #print ("File %s" % self.csv_path)
        self.csv_reader = csv.reader(self.csv_file)
        self.data = []
        self.headers = []
        self.read_csv()
        
    def read_csv(self):
        for i, row in enumerate(self.csv_reader):
            if i == 0:
                self.headers = row
            else:
                self.data.append(row)
                
    def get_data(self):
        return self.data
    
    def getRowCount(self):
        return len(self.data)
    
    def get_headers(self):
        return self.headers

    def get_row(self, index):
        return self.data[index]
    
    def safeString(self, STR):
        if STR is None:
            return ""
        # Decode bytes if necessary and replace non-breaking spaces with regular spaces
        if isinstance(STR, bytes):
            STR = STR.decode("utf-8", errors="ignore")
        STR = STR.replace("\xc2\xa0", " ")  # Replace non-breaking spaces
        STR = re.sub(r'\s+', ' ', STR)  # Replace multiple spaces with a single space
        return STR.strip()    

    def exploreRowsForKeySections(self):
        result = []
        for rid, row in enumerate(self.data):
            KS = self.safeString(row[0])
            if KS.find("STAAR Performance (All Students)") >= 0:
                continue
            if KS.startswith("FLORESVILLE ISD") or KS.startswith("STAAR Performance"):
                continue
            if KS == "":
                continue
            F = True
            for i in range(1, len(row), 1):
                if row[i] != "":
                    F = False
                    break
            if F:
                result.append([rid, KS])
        return result

    def discoverKeySections(self, YEAR):
        leftovers = []
        SECTS = self.exploreRowsForKeySections()
        for SECT in SECTS:
            F = False
            for K in self.key_sections.keys():
                # don't discover things we know aren't there.
                if not YEAR in self.key_sections[K]['years']:
                    continue;
                # Don't discover what we already know
                if self.key_sections[K]["row"] != -1:
                    continue
                # does it start with token
                if SECT[1].startswith(self.key_sections[K]["tag"]):
                    self.key_sections[K]["row"] = SECT[0]
                    F = True
                    break
            if not F:
                print ("Unexpected section %s %s" % (YEAR, SECT[1]))
                leftovers.append(SECT)
                
    def checkKeySections(self, YEAR):
        AllHere = True
        for K in self.key_sections.keys():
            if not YEAR in self.key_sections[K]['years']:
                continue
            if self.key_sections[K]['row'] == -1:
                prettyprinter.pprint(self.key_sections[K])
                H = self.exploreRowsForKeySections()
                prettyprinter.pprint(H)
                AllHere = False
                return AllHere
        return AllHere
    
    
    def getSection(self, section):
        if not section in self.key_sections.keys():
            print ("Section %s not found" % section)
            return None
        result = {}
        RID = self.key_sections[section]["row"]
        if RID == -1:
            print ("Section %s row is -1" % section)
            return {}
        # Move to first data
        RID += 1
        WKROW = self.get_row(RID)
        # 
        ROWTAG = self.safeString(WKROW[0])
        result[ROWTAG] = {}
        YEAR = self.safeString(WKROW[1])
        result[ROWTAG][YEAR] = {}
        for C in self.key_columns.keys():
            result[ROWTAG][YEAR][C] = self.safeString(WKROW[self.key_columns[C]])
        RID += 1
        WKROW = self.get_row(RID)
        YEAR = self.safeString(WKROW[1])
        result[ROWTAG][YEAR] = {}
        for C in self.key_columns.keys():
            result[ROWTAG][YEAR][C] = self.safeString(WKROW[self.key_columns[C]])

        RID += 1
        WKROW = self.get_row(RID)
        ROWTAG = self.safeString(WKROW[0])
        result[ROWTAG] = {}
        YEAR = self.safeString(WKROW[1])
        result[ROWTAG][YEAR] = {}
        for C in self.key_columns.keys():
            result[ROWTAG][YEAR][C] = self.safeString(WKROW[self.key_columns[C]])
        RID += 1
        WKROW = self.get_row(RID)
        YEAR = self.safeString(WKROW[1])
        result[ROWTAG][YEAR] = {}
        for C in self.key_columns.keys():
            result[ROWTAG][YEAR][C] = self.safeString(WKROW[self.key_columns[C]])

        RID += 1
        WKROW = self.get_row(RID)
        ROWTAG = self.safeString(WKROW[0])
        result[ROWTAG] = {}
        YEAR = self.safeString(WKROW[1])
        result[ROWTAG][YEAR] = {}
        for C in self.key_columns.keys():
            result[ROWTAG][YEAR][C] = self.safeString(WKROW[self.key_columns[C]])
        RID += 1
        WKROW = self.get_row(RID)
        YEAR = self.safeString(WKROW[1])
        result[ROWTAG][YEAR] = {}
        for C in self.key_columns.keys():
            result[ROWTAG][YEAR][C] = self.safeString(WKROW[self.key_columns[C]])
        return result
        
    def convertData(self):
        result = {}
        for SECT in self.key_sections.keys():
            if self.key_sections[SECT]['row'] <= 0:
                result[SECT] = {}
                continue
            result[SECT] = self.getSection(SECT)
        return result



    def getScore(self, VSTR):
        VSTR = VSTR.strip()
        if VSTR == "*":
            return -1.0
        VSTR = VSTR.replace("%","").strip()
        try:
            F = float(VSTR)
            return F
        except Exception as E:
            return -1.0

        
    def close(self):
        self.csv_file.close()
        
    def __del__(self):
        self.close()
        
    def __str__(self):
        return f"TEACsvReader: {self.csv_path}"
    
    def __repr__(self):
        return f"TEACsvReader({self.csv_path})"