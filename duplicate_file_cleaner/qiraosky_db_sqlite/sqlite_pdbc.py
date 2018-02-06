# -*- coding: utf-8 -*-
import sqlite3

class SqlitePdbc(object):
    dbpath = ""
    def __init__(self,dbpath):
        self.dbpath = dbpath;
        #print "SqlitePdbc 已初始化完成!"

    def create_conn(self):
        return  sqlite3.connect(self.dbpath)

    def execute(self,sql):
        conn = self.create_conn()
        conn.execute(sql)
        conn.commit()
        conn.close()

    def query(self,sql):
        conn = self.create_conn()
        cursor = conn.execute(sql)
        result = [];
        for row in cursor:
            result.append(row)
        conn.close()
        return result
