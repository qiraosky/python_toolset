# -*- coding:utf-8 -*-
"""
mydump_sched
"""
import time
import os
import json
import base64
import schedule

JSON_PATH = "config.json"
MYSQL_DUMP = "mysqldump"
#MYSQL_DUMP = "D:\\DataBase\\mysql\mysqld\\bin\\mysqldump.exe"
IS_DEBUG = False

def decode(ciphertext):
    """
    decode twice base64
    """
    try:
        return base64.decodestring(base64.decodestring(ciphertext))
    except:
        raise Exception("decode error: please check if the ciphertext is twice transcoding by base64, ciphertext=%s" % ciphertext)

def check_if_is_none(value,message):
    """
    check value 
    """
    if None == value:
        raise Exception("error:%s" % message)

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

def check_key_if_exist(obj, key_name):
    try:
        v = obj[key_name]
        return True
    except:
        return False

def do_backup_job(db_name, mysql_backup_path, time_str, database_ip, database_user, database_pass):
    global MYSQL_DUMP, IS_DEBUG
    cmd = "%s -h%s -u%s -p%s --default-character-set=utf8 %s --skip-lock-tables \
          --extended-insert=false | gzip -c > %s%s_%s.sql.gz" \
          % (MYSQL_DUMP, database_ip, database_user, database_pass,\
           db_name, mysql_backup_path, db_name, time_str)
    os.system(cmd)
    print "mysql dump %s@%s:%s to %s" % (database_user, database_ip, db_name, mysql_backup_path)
    if IS_DEBUG:
        print cmd

def db_config_default_filter(config, db_obj, prop_name):
    '''
    db_obj_filter
    '''
    if prop_name == 'db_name':
        return db_obj["db_name"]
    if prop_name == 'mysql_backup_path':
        return set_default_value(db_obj, "mysql_backup_path", config["mysql_backup_local_path"])
    if prop_name == 'database_ip':
        return set_default_value(db_obj, "database_ip", config["database_ip"])
    if prop_name == 'database_user':
        return set_default_value(db_obj, "database_user", config["database_user"])
    if prop_name == 'database_pass':
        return set_default_value(db_obj, "database_pass", config["database_pass"])


def backup_task(config):
    """
    backup to local
    """
    global IS_DEBUG
    year_str = time.strftime('%Y', time.localtime())
    month_str = time.strftime('%m', time.localtime())
    time_str = time.strftime('%Y%m%d%H%M', time.localtime())

    mysql_backup_path = config["mysql_backup_local_path"]
    year_month_path = mysql_backup_path + year_str + "/" + month_str + "/"
    backup_path = year_month_path + time_str + "/"

    if not os.path.exists(backup_path):
        os.makedirs(backup_path)

    for db_obj in config['dbs']:
        db_name = db_config_default_filter(config, db_obj, "db_name")
        database_ip = db_config_default_filter(config, db_obj, "database_ip")
        database_user = db_config_default_filter(config, db_obj, "database_user")
        database_pass = decode(db_config_default_filter(config, db_obj, "database_pass"))
        do_backup_job(db_name, backup_path, time_str,database_ip, database_user, database_pass)
    return year_str, month_str, backup_path

def mkdir_remote(config, dir_path, passwd, username, host_ip):
    '''
     mk a remote dir
    '''
    global IS_DEBUG
    cmd_str = 'sshpass -p %s ssh %s@%s mkdir -p %s' % (passwd, username, host_ip, dir_path)
    if IS_DEBUG:
        print cmd_str
    os.system(cmd_str)

def offsite_backup_task(config, year_str, month_str, local_backup_path):
    """
    send backup files to offsite server
    """
    global IS_DEBUG
    off_site_year_month_path = config["off_site_backup"]["backup_path"] + year_str + "/" + month_str + "/"
    if IS_DEBUG:
        print off_site_year_month_path
    host_ip = config["off_site_backup"]["host_ip"]
    username = config["off_site_backup"]["username"]
    passwd = decode(config["off_site_backup"]["password"])
    mkdir_remote(config, off_site_year_month_path, passwd, username, host_ip)
    cmd_str = 'sshpass -p %s scp -r %s %s@%s:%s' % (passwd, local_backup_path, username, host_ip, off_site_year_month_path)
    if IS_DEBUG:
        print cmd_str
    os.system(cmd_str)
    print "Transfer to %s@%s:%s backup files is completed!" % (username, host_ip, off_site_year_month_path)

def task(config):
    """
    task
    """
    year_str, month_str, local_backup_path = backup_task(config)
    if check_key_if_exist(config, "off_site_backup"):
        if check_key_if_exist(config, "enabled"):
            if config["off_site_backup"]["enabled"]:
                offsite_backup_task(config, year_str, month_str, local_backup_path)
    print "task completed: %s" % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    print "---------------------------------------------------------------------------------------------->"


def doJobs(config):
    """
    job runner
    """
    schedule.every().day.at(config["task_execution_time"]).do(task,config)
    task(config)
    while True:
        schedule.run_pending()
        time.sleep(1)

def set_config_default_value(key_name, source_obj, target_obj, check_value_if_is_none = False, profix = ""):
    if check_key_if_exist(source_obj,key_name):
        target_obj[key_name] = source_obj[key_name]
    if not check_key_if_exist(target_obj,key_name):
        target_obj[key_name] = None
    if check_value_if_is_none:
        if "" == profix:
            check_if_is_none(target_obj[key_name], "%s is not defined" % (key_name) )
        else:
            check_if_is_none(target_obj[key_name], "%s.%s is not defined" % (profix, key_name) )
    return target_obj[key_name]

def get_profile_config(config):
    """
    use profile config tp reinitialize config object
    """
    profile = config["profile"]["selected"]
    selected_option = config["profile"]["option"][profile]
    # mysql_backup_local_path
    set_config_default_value("mysql_backup_local_path", selected_option, config, True)
    # task_execution_time
    set_config_default_value("task_execution_time", selected_option, config, True)
    # database_ip
    set_config_default_value("database_ip", selected_option, config, True)
    # database_user
    set_config_default_value("database_user", selected_option, config, True)
    # database_pass
    set_config_default_value("database_pass", selected_option, config, True)
    # off_site_backup
    if check_key_if_exist(selected_option, "off_site_backup"):
        selected_option_off_site_backup = selected_option["off_site_backup"]
        if not check_key_if_exist(config,"off_site_backup"):
            config["off_site_backup"] = {}
        config_off_site_backup = config["off_site_backup"]
        # enabled
        set_config_default_value("enabled", selected_option_off_site_backup, config_off_site_backup, True, "off_site_backup")
        # enabled is true
        if config_off_site_backup["enabled"]:
            # host_ip
            set_config_default_value("host_ip", selected_option_off_site_backup, config_off_site_backup, True, "off_site_backup")
            # username
            set_config_default_value("username", selected_option_off_site_backup, config_off_site_backup, True, "off_site_backup")
            # password
            set_config_default_value("password", selected_option_off_site_backup, config_off_site_backup, True, "off_site_backup")
            # backup_path
            set_config_default_value("backup_path", selected_option_off_site_backup, config_off_site_backup, True, "off_site_backup")
    return config


def main():
    """
      main func
    """
    global JSON_PATH, IS_DEBUG
    jsonfile = open(JSON_PATH)
    try:
        config = json.load(jsonfile)
    except:
        raise Exception("config.json JSON format is not correct")
    config = get_profile_config(config)
    if IS_DEBUG:
        config["enabled"] = True
        print config
        print ""
    if config["enabled"]:
        doJobs(config)
    else:
        print "config enabled is false!"
    

main()
