"""
mydump_sched
"""
import time
import os
import json
import base64
import schedule


# local backup config
TASK_EXECUTION_TIME = "03:00"
MYSQL_DUMP = 'mysqldump'
# Note: must have the last slash
MYSQL_BACKUP_PATH = '/cloud/workdir/mysql_backup/'
JSON_PATH = "config.json"


# remote offsite backup server config
OFF_SITE_BACKUP_HOST_IP = "10.11.1.255"
OFF_SITE_BACKUP_USERNAME = "root"
OFF_SITE_BACKUP_PASSWORD = "TVhGaGVrQlhVMWc9"
# Note: must have the last slash
OFF_SITE_BACKUP_BACKUP_PATH = "/cloud/mysql_backup/"



PROFILE = 'dev'
if PROFILE == 'dev':
    DEFAULT_DATABASE_IP = '10.11.1.255'
    DEFAULT_DATABASE_USER = 'devread'
    DEFAULT_DATABASE_PASS = '123456'
elif PROFILE == 'sit':
    DEFAULT_DATABASE_IP = '10.11.2.50'
    DEFAULT_DATABASE_USER = 'appread'
    DEFAULT_DATABASE_PASS = '123456' 
elif PROFILE == 'prod':
    DEFAULT_DATABASE_IP = '10.21.24.221'
    DEFAULT_DATABASE_USER = 'operead'
    DEFAULT_DATABASE_PASS = '123456'
else:
    DEFAULT_DATABASE_IP = '10.11.1.255'
    DEFAULT_DATABASE_USER = 'devread'
    DEFAULT_DATABASE_PASS = '123456'



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
      set default value
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

def mkdir_remote(dir_path):
    '''
     mk a remote dir
    '''
    global OFF_SITE_BACKUP_HOST_IP, OFF_SITE_BACKUP_USERNAME, OFF_SITE_BACKUP_PASSWORD
    cmd_str = 'sshpass -p %s ssh %s@%s mkdir -p %s' % (base64.decodestring(base64.decodestring(
        OFF_SITE_BACKUP_PASSWORD + '\n')), OFF_SITE_BACKUP_USERNAME, OFF_SITE_BACKUP_HOST_IP, dir_path)
    os.system(cmd_str)

def task():
    '''
     task
    '''
    global JSON_PATH, MYSQL_BACKUP_PATH, OFF_SITE_BACKUP_USERNAME, OFF_SITE_BACKUP_PASSWORD, OFF_SITE_BACKUP_BACKUP_PATH, OFF_SITE_BACKUP_HOST_IP
    with open(JSON_PATH) as json_file:
        data = json.load(json_file)
        year_str = time.strftime('%Y', time.localtime())
        month_str = time.strftime('%m', time.localtime())
        time_str = time.strftime('%Y%m%d%H%M', time.localtime())

        mysql_backup_path = MYSQL_BACKUP_PATH
        year_month_path = mysql_backup_path + year_str + "/" + month_str + "/"
        off_site_year_month_path = OFF_SITE_BACKUP_BACKUP_PATH + year_str + "/" + month_str + "/"
       
        backup_path = year_month_path + time_str + "/"
        for db_obj in data['dbs']:
            db_name = db_obj_filter(db_obj, "db_name")
            database_ip = db_obj_filter(db_obj, "database_ip")
            database_user = db_obj_filter(db_obj, "database_user")
            database_pass = db_obj_filter(db_obj, "database_pass")

            if not os.path.exists(backup_path):
                os.makedirs(backup_path)
            job(db_name, backup_path, time_str,
                database_ip, database_user, database_pass)
        mkdir_remote(backup_path)
        cmd_str = 'sshpass -p %s scp -r %s %s@%s:%s' % (base64.decodestring(base64.decodestring(
            OFF_SITE_BACKUP_PASSWORD + '\n')), backup_path, OFF_SITE_BACKUP_USERNAME, OFF_SITE_BACKUP_HOST_IP, off_site_year_month_path)
        os.system(cmd_str)


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


