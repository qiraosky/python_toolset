"""
mydump_sched
"""
import time
import os
import schedule


DATABASE_LIST = ['db_name']
MYSQL_DUMP = 'D:\\DataBase\\mysql\\mysqld\\bin\\mysqldump'
MSYQL_BACKUP_PATH = 'D:\\cloud\\msyqlbackup\\'
DATABASE_IP = '10.11.1.100'
DATABASE_USER = 'appread'
DATABASE_PASS = '123456'





def job(db_name, msyql_backup_path, time_str, database_ip, database_user, database_pass):
    '''
     job
    '''
    global MYSQL_DUMP
    cmd = "%s -h%s -u%s -p%s --default-character-set=utf8 %s --skip-lock-tables \
          --extended-insert=false | gzip -c > %s%s_%s.sql.gz" \
          % (MYSQL_DUMP, database_ip, database_user, database_pass,\
           db_name, msyql_backup_path, db_name, time_str)
    os.system(cmd)
    #print "call %s" % cmd


def task():
    '''
     task
    '''
    global MSYQL_BACKUP_PATH, DATABASE_LIST, DATABASE_IP, DATABASE_USER, DATABASE_PASS
    db_list = DATABASE_LIST
    time_str = time.strftime('%Y%m%d%H%M%S', time.localtime())
    backup_path = MSYQL_BACKUP_PATH + \
        time_str + "/"
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)
    for db_name in db_list:
        if db_name == 'saas_information':
            job(db_name, backup_path, time_str,
                DATABASE_IP, DATABASE_USER, DATABASE_PASS)
        else:
            job(db_name, backup_path, time_str,
                DATABASE_IP, DATABASE_USER, DATABASE_PASS)

def main():
    '''
      main func
    '''
    task()
    return
    schedule.every().day.at("14:01").do(task)
    while True:
        schedule.run_pending()
        time.sleep(1)


main()
