import os
import sys

"""
    :copyright: (c)2023 by Russell Dickerson
    :license: MIT, see LICENSE for details
"""

import sqlite3
from sqlite3 import Row 
from json import loads as json_loads

import datetime
from datetime import datetime
from dateutil.parser import parse as date_parser
import traceback
import prettyprinter

class dbStringBuff(object):
    def __init__(self, startup=None):
        if startup != None:
            self.buff = startup
        else:
            self.buff = ""

    def add(self, strpart):
        self.buff += strpart 

    def get(self):
        return self.buff

class   Sqlite3GenericDatabase(object):
    '''
    This class is a wrapper for the Sqlite3 data table access.  It provides generic functions to support the access and 
    simplify the client code.

    Args:
        SQLITEFILE  :   File containing the data table
        OLDHANDLE   :   Shared handle to the SQLITE Database file that's open.

    Example use:
        class StateTotalsDatabase(Sqlite3GenericDatabase):
            def __init__(self, OLDHANDLE = None):
                super(StateTotalDBClass,self).__init__("VAERSByState.db", OLDHANDLE)

    Field types can be INTEGER, VARCHAR(...), CHAR, TEXT, REAL, FLOAT, DATE, DATETIME

    fieldmap is an array of column descriptor.  Each row is a dict containing:
        name - field name
        type - type string
        required - True will add  "NOT NULL"
        indexed - True, an index is created for it
        foreign - if defined, then this field is a foreign key reference to another table. 
                  example: "tablename(field)"
    '''

    def __init__(self, SQLITEFILE : str, OLDHANDLE = None):
        self.DBHANDLE = None    # Database handle
        self.tablename = None   # Table Name
        if OLDHANDLE == None:
            try:
                self.DBHANDLE = sqlite3.connect(SQLITEFILE)
            except Exception as ex:
                print ("Unable to open the database '%s' - %s" % (SQLITEFILE, ex))
                raise ex
        else:
            self.DBHANDLE = OLDHANDLE                       # Reuse the existing handle

        self.fieldmap = [
#            {'name' : 'recno', 'type' : 'INTEGER PRIMARY KEY AUTOINCREMENT', 'required' : None},
#            {'name' : 'primary', 'type' : 'TEXT', 'required' : True},
#            {'name' : 'secondary', 'type' : 'INTEGER', 'required' : False}
        ]

    def getHandle(self):
        return self.DBHANDLE

    def options2Insert(self, OPTS) -> list:
        fields = OPTS.keys()
        fields_str = ",".join(fields)
        vars = [":" + x for x in fields]
        vars_str = ",".join(vars)
        return (fields_str, vars_str)

    def options2Update(self, OPTS) -> str:
        fields = OPTS.keys()
        result = ""
        worklist = [x + "=:" + x for x in fields]
        return ",".join(worklist)

    def makeInsertSQL(self, OPTS: dict) -> str:
        (fields_str, vars_str) = self.options2Insert(OPTS)
        sqlstring = "INSERT INTO %s (%s) values (%s)" % (self.tablename, fields_str, vars_str) 
        return sqlstring

    def makeUpdateSQL(self, OPTS : dict, WHERE : str) -> str:
        fields_str = self.options2Update(OPTS)
        sqlstring = "UPDATE %s SET %s WHERE %s" % (self.tablename, fields_str, WHERE) 
        return sqlstring

    def dropTable(self):
        '''
        DROP the table.
        '''
        SQL = "DROP TABLE IF EXISTS " + self.tablename
        try:
            self.DBHANDLE.execute(SQL)
        except Exception as ex:
            # assume already gone
            return True
        self.DBHANDLE.commit()
        return True

    def tableExists(self):
        SQL = "SELECT name FROM sqlite_master WHERE type='table' and name='%s'" %  self.tablename
        CURSOR = self.DBHANDLE.execute(SQL)
        for row in CURSOR:
            return True
        return False

    # override for each class
    def _makeCreateSQL(self) -> str:
        SQL = "CREATE TABLE %s (" % self.tablename
        SUB = ""
        for field in self.fieldmap:
            if SUB != "":
                SUB += ",\n"
            SUB += "%s %s" % (field['name'], field['type'])
            if field.get('unique', False) == True:
                SUB += " UNIQUE "
            if field['required'] == True:
                SUB += " NOT NULL"
            if field.get('foreign', None) != None:
                SUB += ",\n"
                SUB += "FOREIGN KEY (%s) REFERENCES %s" % (field['name'], field['foreign'])
        SQL += "%s)" % SUB
        return SQL

    def _makeIndexSQL(self) -> list:
        result = []
        N = 0
        for field in self.fieldmap:
            if field.get('indexed', False) == True:
                result.append("CREATE INDEX %s_par_ndx%d ON %s(%s)" % (self.tablename, N, self.tablename, field['name']))
                N += 1
        return result


    def createTable(self):
        SQL = self._makeCreateSQL()
        try:
            CURSOR = self.DBHANDLE.execute(SQL)
            print ("cursor %s" % CURSOR)
        except Exception as ex:
            print ("Error creating table '%s' - %s" % (self.tablename, ex))
            print ("SQL: %s" % SQL)
            raise ex

        ndxlist = self._makeIndexSQL()
        for SQL in ndxlist:
            try:
                self.DBHANDLE.execute(SQL)
            except Exception as ex:
                print ("Error creating table index '%s'  - %s" % (self.tablename, ex))
                print ("SQL: %s" % SQL)
                raise ex
        self.DBHANDLE.commit()
        return True


    # Populate in the subclass.
    def populateTable(self):
        return

    def checkMakeTable(self):
        if self.tableExists() == False:
            self.createTable()
            self.populateTable()
        return True

    def row2rec(self, ROW : dict) -> dict:
        '''
        row2rec takes a row from a query and creates a non-database dict containing the data.
        '''
        copyrec = {}
        for fx in ROW.keys():
            copyrec[fx] = ROW[fx]
        return copyrec


    # Generic SQL query
    def sqlQuery(self, SQL : str, OPTS={}) -> list:
        CURSOR = self.DBHANDLE.execute(SQL, OPTS)
        CURSOR.row_factory = sqlite3.Row
        RET = []
        for row in CURSOR:
            RET.append(self.row2rec(row))
        return RET

    def getAllRecords(self) -> list:
        return self.sqlQuery("SELECT * FROM %s" % self.tablename)

    # WHERE: "field1 = :field1"
    # Pass the value of field1 in the OPTS
    def recordExists(self, WHERE : str, OPTS : dict):
        SQL = "SELECT * FROM " + self.tablename + " WHERE %s" % WHERE
        CURSOR = self.DBHANDLE.execute(SQL, OPTS)
        for row in CURSOR:
            return True
        return False

    # Is this the same as the other, for the fields listed.
    def compareRecs(self, OLD, NEW, FLDS : list):
        for F in FLDS:
            if OLD[F] != NEW[F]:
                return False
        return True

    # Is this list of records the same as the other list, for the fields listed.
    def compareRecLists(self, OLD, NEW, FLDS : list):
        if len(OLD) != len(NEW):
            return False
        for I in range(0, len(OLD), 1):
            if self.compareRecs(OLD[I], NEW[I], FLDS) == False:
                return False 
        return True

    # getRec("field1 = :field1", {"field1" : 123})
    # getRec("field1 = :field1", {"field1" : 123}, ['field1', 'field2', 'field3'])
    # getRec("field1 = :field1", {"field1" : 123}, ['field1', 'field2', 'field3'], "field2 ASC")
    def getRec(self, WHERE : str, OPTS : dict, FIELDS="*", ORDERBY=None):
        SO = dbStringBuff("SELECT ")
        if FIELDS != "*":
            FIELDSTR = ",".join(FIELDS)
            SO.add(FIELDSTR)
        else:
            SO.add(FIELDS)
        SO.add(" FROM %s WHERE " % self.tablename)
        SO.add(WHERE)
        if ORDERBY != None:
            SO.add(" ORDER BY %s" % ORDERBY)
        CURSOR = self.DBHANDLE.execute(SO.get(), OPTS)
        CURSOR.row_factory = sqlite3.Row
        RET = []
        for row in CURSOR:
            RET.append(self.row2rec(row))
        return RET

    def getLikeRecBeginning(self, FIELD : str, VAL : str, ORDERBY=None) -> list:
        OPTS = {'like' : VAL + "%%"}
        SQL = 'SELECT * FROM ' + self.tablename + ' WHERE %s LIKE :like' % FIELD
        if ORDERBY != None:
            SQL += " ORDER BY %s" % ORDERBY
        CURSOR = self.DBHANDLE.execute(SQL, OPTS)
        CURSOR.row_factory = sqlite3.Row
        RET = []
        for row in CURSOR:
            RET.append(self.row2rec(row))
        return RET

    def getLikeRecEnd(self, FIELD : str, VAL : str, ORDERBY=None) -> list:
        OPTS = {'like' : "%%" + VAL}
        SQL = 'SELECT * FROM ' + self.tablename + ' WHERE %s LIKE :like' % FIELD
        if ORDERBY != None:
            SQL += " ORDER BY %s" % ORDERBY
        CURSOR = self.DBHANDLE.execute(SQL, OPTS)
        CURSOR.row_factory = sqlite3.Row
        RET = []
        for row in CURSOR:
            RET.append(self.row2rec(row))
        return RET

    def getLikeRecAnywhere(self, FIELD : str, VAL, ORDERBY = None) -> list:
        OPTS = {'like' : "%%" + VAL + "%%"}
        SQL = 'SELECT * FROM ' + self.tablename + ' WHERE %s LIKE :like' % FIELD
        if ORDERBY != None:
            SQL += " ORDER BY %s" % ORDERBY
        CURSOR = self.DBHANDLE.execute(SQL, OPTS)
        CURSOR.row_factory = sqlite3.Row
        RET = []
        for row in CURSOR:
            RET.append(self.row2rec(row))
        return RET
    
    def addRec(self, OPTS : dict):
        ofields = OPTS.keys()
        for field in self.fieldmap:
            if field['required'] == True:
                if not field['name'] in ofields:
                    return [False, "Required field %s is missing in data" % field['name']]
            elif field['required'] == None:
                # auto-increment shouldn't be included in an add or update.
                if field['name'] in ofields:
                    OPTS.pop(field['name'], None)
        SQL = self.makeInsertSQL(OPTS)
        try:
            self.DBHANDLE.execute(SQL, OPTS)
        except Exception as ex:
            print ("Unable to add record to %s - %s" % (self.tablename, ex))
            prettyprinter.pprint(OPTS)
            print ("SQL: %s" % SQL)
            if self.FAILONERROR:
                raise ex
            return False
        self.DBHANDLE.commit()
        return True


    def updateRec(self, OPTS : dict, WHERE : str):
        SQL = self.makeUpdateSQL(OPTS, WHERE)
        try:
            self.DBHANDLE.execute(SQL, OPTS)
        except Exception as ex:
            print ("Unable to update record to %s - %s" % (self.tablename, ex))
            prettyprinter.pprint(OPTS)
            print ("SQL: %s" % SQL)
            if self.FAILONERROR:
                raise ex
            else:
                return False
        self.DBHANDLE.commit()
        return True

    def deleteAll(self):
        SQL = "DELETE FROM " + self.tablename
        try:
            self.DBHANDLE.execute(SQL)
        except Exception as ex:
            print ("Unable to delete records for %s - %s" % (self.tablename, ex))
            if self.FAILONERROR:
                raise ex
            else:
                return False
        self.DBHANDLE.commit()
        return True

    def deleteByRecid(self, RECID : int):
        SQL = "DELETE FROM " + self.tablename + " WHERE recno=:recno"
        OPTS = {'recno' : RECID}
        try:
            self.DBHANDLE.execute(SQL, OPTS)
        except Exception as ex:
            print ("Unable to delete records for %s - %s" % (self.tablename, ex))
            print ("SQL: %s" % SQL)
            return False
        self.DBHANDLE.commit()
        return True

    def deleteByWhere(self, WHERE : str, OPTS : list):
        SQL = "DELETE FROM " + self.tablename + " WHERE %s" % WHERE
        try:
            self.DBHANDLE.execute(SQL, OPTS)
        except Exception as ex:
            print ("Unable to delete record for %s - %s" % (self.tablename, ex))
            print ("SQL: %s" % SQL)
            return False
        self.DBHANDLE.commit()
        return True

