# -*- coding: utf-8 -*-
import qiraosky_db_sqlite.sqlite_pdbc as pdbc
import FileEntityOper
import datetime,time
import os
import hashlib


def get_file_md5( filepath):
    if os.path.isfile(filepath):
        f = open(filepath, 'rb')
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        f.close()
        return str(hash).upper()
    return None

# md5code = get_file_md5("D:\\test\\tianee\\tianee\\thirdparty\\newcapec\\cas\\service\\casService.class")
# print md5code

def main():
    sourcePath = 'D:\\test'
    targetPath = ""
    print  "源文件夹：" + sourcePath
    print  "目标文件夹：" + targetPath
    print  "文件扫描程序已启动......"
    for root, dits, files in os.walk(sourcePath):
        for i in files:
            rootUtf8 = root.decode('gbk').encode('UTF-8')
            fileName = i.decode("gbk").encode('UTF-8')
            filepath = rootUtf8 + "\\" + fileName
            fileattr = ""
            #得到文件属性
            try:
                fileattr = os.stat(filepath)
            except:
                pass
            #文件属性为空，则返回
            if fileattr == '':
                continue
            #st_atime (访问时间), st_mtime (修改时间), st_ctime（创建时间）

            #得到文件 md5
            file_md5 = get_file_md5(filepath);
            #无法识别文件md5码
            if None == file_md5:
                continue
            #文件操作对象
            fileOper = FileEntityOper.FileEntityOper();

            fileMd5List = fileOper.get_file_entity_by_md5code(file_md5)
            if len(fileMd5List)!=0:
                print filepath + '已存在'
                time.sleep(0.01)
                continue

            time.sleep(0.1)
            fileEntity = FileEntityOper.FileEntity();
            fileEntity.name = fileName;
            fileEntity.md5code = file_md5
            fileEntity.suffix = "";
            fileEntity.create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(fileattr.st_ctime))
            fileEntity.update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(fileattr.st_mtime))
            fileEntity.oper_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            fileEntity.status = "1";
            fileEntity.comment = filepath;
            fileEntity.desc = "";
            print fileEntity.to_string()
            try:
                fileOper.insert(fileEntity)
            except:
                print filepath + "处理出错"
            time.sleep(0.01)
    print  "文件扫描程序已完成！"



main();










