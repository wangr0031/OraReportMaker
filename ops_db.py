#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wangrong'
import cx_Oracle
from ora_logger import logger


class OpsDb():
    def __init__(self, db_username, db_password, db_dns,con_mode=None):
        self.db_username = db_username
        self.db_password = db_password
        self.db_dns = db_dns
        self.cx_con=self.connect_db(con_mode)

    def connect_db(self, con_mode=None):
        try:
            cx_con = cx_Oracle.connect(self.db_username, self.db_password, self.db_dns, con_mode)
            logger.info("Connect to Database Success!")
        except Exception as err:
            logger.error("Connect to Database [username={},password={},ora_dsn={}] get error!".format(self.db_username,
                                                                                                     self.db_password,
                                                                                                     self.db_dns))
            logger.error("error:{}".format(err))
        return cx_con

    def insert_data(self,insert_sql):
        pass

    def update_data(self,update_sql):
        pass

    def delete_data(self,delete_sql):
        pass

    def select_data(self,select_sql):
        pass

    def export_data_from_table(self,table_name):
        pass

    def export_awr_report(self):
        pass

    def export_ash_report(self):
        pass

    def export_addm_report(self):
        pass
