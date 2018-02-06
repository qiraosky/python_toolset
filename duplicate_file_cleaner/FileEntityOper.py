# -*- coding: utf-8 -*-
import qiraosky_db_sqlite.sqlite_pdbc as pdbc

#文件实体
class FileEntity(object):
    id=""
    name=""
    md5code=""
    suffix=""
    create_time=""
    update_time=""
    oper_time=""
    status=""
    comment=""
    desc=""
    def to_string(self):
        return  "id="+str(self.id)+",name="+self.name+",md5code="+self.md5code+",suffix="+self.suffix\
                +",create_time="+str(self.create_time)+",update_time="+str(self.update_time)+",oper_time="\
                +str(self.oper_time)+",status="+self.status+",comment="+self.comment+",desc="+self.desc
    def __init__(self):
        pass

#
class FileEntityOper(object):
    def __init__(self):
        pass
    def get_file_entity_by_md5code(self,md5code):
        sqlconn = pdbc.SqlitePdbc('db/db.db');
        result = sqlconn.query("select * from tq_file where md5code= '"+md5code+"'")
        fileEntityList = [];
        for row in result:
            fileEntity = FileEntity();
            fileEntity.id = row[0]
            fileEntity.name = row[1]
            fileEntity.md5code = row[2]
            fileEntity.suffix = row[3]
            fileEntity.create_time = row[4]
            fileEntity.update_time = row[5]
            fileEntity.oper_time = row[6]
            fileEntity.status = row [7]
            fileEntity.desc = row[8]
            fileEntityList.append(fileEntity)
        return fileEntityList
    def insert(self,fileEntity):
        sqlconn = pdbc.SqlitePdbc('db/db.db');
        sqlconn.execute('INSERT INTO "main"."tq_file" ("name", "md5code","suffix", "create_time", "update_time", "oper_time", "status", "comment", "desc")' + \
                        '  VALUES ("'+fileEntity.name+'", "'+fileEntity.md5code+'","'+fileEntity.suffix+'", "'+str(fileEntity.create_time)+\
                        '", "'+str(fileEntity.update_time)+'", "'+str(fileEntity.oper_time)+'", "'+fileEntity.status+'", "'+fileEntity.comment+'", "'+fileEntity.desc+'")')


