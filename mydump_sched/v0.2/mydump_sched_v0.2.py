"""
mydump_sched
"""
import time
import os
import json
import base64
import schedule


TASK_EXECUTION_TIME = "03:00"
MYSQL_DUMP = 'mysqldump'
MYSQL_BACKUP_PATH = '/cloud/mydump_sche/mysql_backup/'
JSON_PATH = "json/dbs.json"


DEFAULT_DATABASE_IP = '10.0.0.1'
DEFAULT_DATABASE_USER = 'operead'
DEFAULT_DATABASE_PASS = 'cloud1q2wdata'



def job(db_name, mysql_backup_path, time_str, database_ip, database_user, database_pass):
    '''
     job
    '''
    global MYSQL_DUMP
    cmd = "%s -h%s -u%s -p%s --default-character-set=utf8 %s --skip-lock-tables \
          --extended-insert=false | gzip -c > %s%s_%s.sql.gz" \
          % (MYSQL_DUMP, database_ip, database_user, database_pass,\
           db_name, mysql_backup_path, db_name, time_str)
    os.system(cmd)
    print "%s" % cmd


def set_default_value(db_obj, prop_name, default_value):
    '''
    '''
    try:
        value = db_obj[prop_name]
        if value is None:
            return default_value
        else:
            return value
    except:
        return default_value



def db_obj_filter(db_obj, prop_name):
    '''
    db_obj_filter
    '''
    global MYSQL_BACKUP_PATH, DEFAULT_DATABASE_IP, DEFAULT_DATABASE_USER, DEFAULT_DATABASE_PASS
    if prop_name == 'db_name':
        return db_obj["db_name"]
    if prop_name == 'mysql_backup_path':
        return set_default_value(db_obj, "mysql_backup_path", MYSQL_BACKUP_PATH)
    if prop_name == 'database_ip':
        return set_default_value(db_obj, "database_ip", DEFAULT_DATABASE_IP)
    if prop_name == 'database_user':
        return set_default_value(db_obj, "database_user", DEFAULT_DATABASE_USER)
    if prop_name == 'database_pass':
        return set_default_value(db_obj, "database_pass", DEFAULT_DATABASE_PASS)
    return None


def task():
    '''
     task
    '''
    global JSON_PATH, MYSQL_BACKUP_PATH
    with open(JSON_PATH) as json_file:
        data = json.load(json_file)
        time_str = time.strftime('%Y%m%d%H%M%S', time.localtime())
	    mysql_backup_path = MYSQL_BACKUP_PATH
        backup_path = mysql_backup_path + time_str + "/" 
	for db_obj in data['dbs']:
            db_name = db_obj_filter(db_obj, "db_name")
            database_ip = db_obj_filter(db_obj, "database_ip")
            database_user = db_obj_filter(db_obj, "database_user")
            database_pass = db_obj_filter(db_obj, "database_pass")

            if not os.path.exists(backup_path):
                os.makedirs(backup_path)
            job(db_name, backup_path, time_str,
                database_ip, database_user, database_pass)
        os.system('sshpass -p %s scp -r %s root@10.0.0.2:/cloud/mydump_sche/mysql_backup/' % (base64.decodestring(base64.decodestring('YUdWc2JHOWhZV0U9')), backup_path))


def main():
    '''
      main func
    '''
    global TASK_EXECUTION_TIME
    schedule.every().day.at(TASK_EXECUTION_TIME).do(task)
    task()
    while True:
        schedule.run_pending()
        time.sleep(1)


main()
