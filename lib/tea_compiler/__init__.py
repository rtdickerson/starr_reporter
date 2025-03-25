import os
import sys 
import prettyprinter
import csv
import numpy as np
import re  # Add this import at the top of the file
import io

from tea_csv_reader import TEACsvReader

class TEADataCompiler:
    
    def loadData(self, YEAR, FILE):
        self.reader = TEACsvReader(FILE)
        self.reader.discoverKeySections(YEAR)
        return self.reader.convertData()
    
    def __init__(self):
        self.YEARS = [2018,2019,2020,2021,2022,2023,2024]
        self.sections = None
        self.INPUT = {
            "2018-2019" : { "file" : "tea_reports/STARR_TEA_TPRS - STAAR FISD 2018-2019.csv",
                           "years" : [2018, 2019],
            }, 
            "2020-2021" : { "file" : "tea_reports/STARR_TEA_TPRS - STARR FISD 2020-2021.csv",
                           "years" : [2019, 2021],
            },
            "2021-2022" : { "file" : "tea_reports/STARR_TEA_TPRS - STARR FISD 2021-2022.csv",
                           "years" : [2021, 2022],
            },
            "2022-2023" : { "file" : "tea_reports/STARR_TEA_TPRS - STARR FISD 2022-2023.csv",
                           "years" : [2022, 2023],
            },
            "2023-2024" : { "file" : "tea_reports/STARR_TEA_TPRS - STARR FISD 2023-2024.csv",
                           "years" : [2023, 2024],
            }
        }
        self.KEEP_COLUMNS = [
            "TEXAS", "REGION20", "FISD", 'African American', 'Hispanic', 'White',
            'Two or More Races', 'Special Ed', 'Econ Disadv', 'EB/EL'
        ]
        self.LOADED = {}
        for YEAR in self.INPUT.keys():
            self.LOADED[YEAR] = self.loadData(YEAR, self.INPUT[YEAR]['file'])
        
    def breakUpScores(self, Approaches,Met,Mastered):
        solid_fail = 100.0 - Approaches
        near_miss = Approaches - Met
        met = Met - Mastered
        mastered =  Mastered
        return {
            "solid_fail" : solid_fail,
            "near_miss" : near_miss,
            "met" : met,
            "mastered" : mastered
        }        
            
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
    
    def getResultForYearSection(self, YEAR, SECTION):
        result = {}
        (YEAR1, YEAR2) = self.INPUT[YEAR]['years']
        result["%d" % YEAR1] = {}
        result["%d" % YEAR2] = {}
        if (not YEAR in self.reader.key_sections[SECTION]['years']):
            # No data in STARR for this topic this year
            result["%d" % YEAR1] = {}
            result["%d" % YEAR2] = {}
            return result
        for PART in [["approaches", "At Approaches Grade Level or Above"],
                  ["met", "At Meets Grade Level or Above"],
                  ["master", "At Masters Grade Level"]
                  ]:
            ROW = self.LOADED[YEAR][SECTION][PART[1]]["%d" % YEAR1]
            LINE = {}
            for K in ROW.keys():
                LINE[K] = self.getScore(ROW[K])
            result["%d" % YEAR1]["%s" % PART[0]] = LINE
            ROW = self.LOADED[YEAR][SECTION][PART[1]]["%d" % YEAR2]
            LINE = {}
            for K in ROW.keys():
                LINE[K] = self.getScore(ROW[K])
            result["%d" % YEAR2]["%s" % PART[0]] = LINE
        return result
    
    def transformYearSection(self, YEAR, SECTION):
        resp = self.getResultForYearSection(YEAR, SECTION)
        (YEAR1, YEAR2) = self.INPUT[YEAR]['years']
        if resp["%d" % YEAR1] == {}:
            # Blank years return None, there's nothing to do.
            return None
        COLS = resp["%d" % YEAR1]["approaches"].keys()
        result = {}
        for YR in self.INPUT[YEAR]['years']:
            for COL in COLS:
                if not COL in self.KEEP_COLUMNS:
                    continue
                if result.get(COL,None) == None:
                    result[COL] = {}
                AP = resp["%d" % YR]['approaches'][COL]
                ME = resp["%d" % YR]['met'][COL]
                MA = resp["%d" % YR]['master'][COL]
                if AP < 0.0:
                    result[COL]["%d" % YR] = {}
                    continue       
                scores = self.breakUpScores(AP,ME,MA)
                result[COL]["%d"%YR] = scores
        return result        
    
    def collectSectionAcrossTime(self, SECTION):
        result = {}
        for YEAR in self.INPUT.keys():
            resp = self.transformYearSection(YEAR, SECTION)
            if resp == None:
                continue
            for CAT in resp.keys():
                if result.get(CAT, None) == None:
                    result[CAT] = {}
                for RYR in resp[CAT].keys():
                    #if the year does not exist, add it
                    if result[CAT].get(RYR, None) == None:
                        result[CAT][RYR] = resp[CAT][RYR]
        return result

    def collectionToCsv(self, SECTION):
        resp = self.collectSectionAcrossTime(SECTION)
        TITLE = self.reader.key_sections[SECTION]['tag']
        output = io.StringIO()
        csv_writer = csv.writer(output, lineterminator="\n")
        csv_writer.writerow([TITLE])
        ROW = [""]
        YEARS = None
        # Make the category 1stlevel groups
        for CAT in resp.keys():
            if YEARS == None:
                YEARS = resp[CAT].keys()
            ROW += [CAT, "","","", "",""]
        csv_writer.writerow(ROW)
        # Make category detail line
        ROW = ["Year"]
        for CAT in resp.keys():
            if YEARS == None:
                YEARS = resp[CAT].keys()
            ROW += ["HardFail", "NearFail","Met","Master","Pass","Fail"]
        csv_writer.writerow(ROW)
        # Make data
        for YEAR in YEARS:
            ROW = [YEAR]
            #    'EB/EL': {
            #       '2018': {
            #           'solid_fail': 42.0,
            #           'near_miss': 42.0,
            #           'met': 11.0,
            #           'mastered': 5.0
            #       },

            for CAT in resp.keys():
                if resp[CAT][YEAR] == {}:
                    ROW += ["", "", "", "", "",""]
                    continue
                ROW += [resp[CAT][YEAR]['solid_fail'], resp[CAT][YEAR]['near_miss'],
                        resp[CAT][YEAR]['met'], resp[CAT][YEAR]['mastered'],
                        resp[CAT][YEAR]['met'] + resp[CAT][YEAR]['mastered'],
                        resp[CAT][YEAR]['solid_fail'] + resp[CAT][YEAR]['near_miss'],
                        ]
            csv_writer.writerow(ROW)
        
        result = output.getvalue()
        output.close()
        return result

    #
    # LOADED -> 2018-2019 -> section-token -> 
    def getSection(self, SECT):
        for SET in self.LOADED.keys():
            for PART in self.LOADED[SET]['grade3-reading'].keys():
                print ("%s grade3-reading %s" % (SET,  self.LOADED[SET]['grade3-reading']))