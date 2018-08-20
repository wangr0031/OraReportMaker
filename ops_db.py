#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wangrong'
import cx_Oracle
from ora_logger import logger
import yaml


class OpsDb():
    def __init__(self, db_username, db_password, db_dns, con_mode=None):
        self.db_username = db_username
        self.db_password = db_password
        self.db_dns = db_dns
        self.cx_con = self.connect_db(con_mode)

    def connect_db(self, con_mode):
        try:
            if con_mode is not None:
                cx_con = cx_Oracle.connect(self.db_username, self.db_password, self.db_dns, mode=con_mode)
            else:
                cx_con = cx_Oracle.connect(self.db_username, self.db_password, self.db_dns)
            logger.info("Connect to Database Success!")
        except Exception as err:
            logger.error("Connect to Database [username={},password={},ora_dsn={}] get error!".format(self.db_username,
                                                                                                      self.db_password,
                                                                                                      self.db_dns))
            logger.error("error:{}".format(err))
            exit()
        return cx_con

    def dml_data(self, db_con_instance, dml_sql, strip_word=';'):
        db_cursor = db_con_instance.cursor()
        try:
            db_cursor.execute(dml_sql.strip(strip_word))
            db_con_instance.commit()
            logger.info("Execute DML statement <{}> success and commit".format(dml_sql.strip(strip_word)))
            db_cursor.close()
        except Exception as err:
            logger.error("Execute DML statement [{}] get error.".format(dml_sql))
            logger.error("error info:\n{}".format(err))
            db_con_instance.rollback()
            db_cursor.close()
            exit()

    def ddl_data(self, db_con_instance, ddl_sql, strip_word=';'):
        db_cursor = db_con_instance.cursor()
        print("ddl = ", ddl_sql.strip(strip_word))
        try:
            logger.debug("Execute DDL statement <{}>".format(ddl_sql))
            # db_cursor.execute(ddl_sql.strip(strip_word))
        except Exception as err:
            logger.error("Execute DDL statement [{}] get error.".format(ddl_sql))
            logger.error("error info:\n{}".format(err))
            db_cursor.close()
            exit()

    def select_data(self, db_con_instance, select_sql, strip_word=';'):
        db_cursor = db_con_instance.cursor()
        try:
            db_cursor.execute(select_sql.strip(strip_word))
            select_result = db_cursor.fetchall()
        except Exception as err:
            logger.error("Execute SELECT statement <{}> get error.".format(select_sql))
            logger.error("error info:\n{}".format(err))
            db_cursor.close()
            exit()
        return select_result

    def export_data_from_table(self, table_name):
        pass

    ##导出AWR报告
    def export_awr_report(self):
        '''
1、根据取AWR报告的时间范围，查出快照ID；

SELECT *
  FROM DBA_HIST_SNAPSHOT T
 WHERE T.END_INTERVAL_TIME >=
       TO_DATE('2017-10-09 09:00:00', 'yyyy-MM-dd hh24:mi:ss')
   AND T.END_INTERVAL_TIME <=
       TO_DATE('2017-10-09 10:01:00', 'yyyy-MM-dd hh24:mi:ss')
 ORDER BY SNAP_ID;
2、利用第一步的END_INTERVAL_TIME,SNAP_ID,DBID,INSTANCE_NUMBER生成报告
SELECT *
  FROM TABLE(DBMS_WORKLOAD_REPOSITORY.AWR_REPORT_HTML(1700577032,
                                                      1,
                                                      38247,
                                                      38251,
                                                      0));
或者：
SELECT DBMS_WORKLOAD_REPOSITORY.AWR_REPORT_HTML(1700577032,
                                                      1,
                                                      38247,
                                                      38251,
                                                      0) FROM dual;
3、把结果粘贴到一个txt中，比如a.txt保存退出。然后改此文件后缀为html,比如a.html.
最后用浏览器打开a.html即可 ，如果需要生成txt格式的报告，
则用DBMS_WORKLOAD_REPOSITORY.AWR_REPORT_TEXT这个函数即可
https://blog.csdn.net/xuemeilu/article/details/78180615?locationNum=9&fps=1
        :return:
        '''
        pass

    ##导出ASH报告
    def export_ash_report(self):
        pass

    def export_addm_report(self):
        pass

    def clean_db_schema_by_user(self):
        with open('CONF/drop_db_schema_by_user_with_sql.cfg', 'rb') as f:
            sql_cfg = yaml.load(f)
        for drop_type in sql_cfg['drop_obj']:
            for onesql in sql_cfg['drop_obj'][drop_type]:
                print("Process drop_type", drop_type)
                logger.info("Clean DB_type {}".format(drop_type))
                db_result_rows = self.select_data(self.cx_con, onesql)
                if db_result_rows:
                    for row in db_result_rows:
                        # print ("row=",'.'.join(row))
                        self.ddl_data(self.cx_con, '.'.join(row))


if __name__ == '__main__':
    o = OpsDb('cpc', '1jian8Shu!', '172.16.80.11:11521/cc')
    o.clean_db_schema_by_user()
