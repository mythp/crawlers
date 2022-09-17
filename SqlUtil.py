import logging
import pymysql
import time


class SqlUtil(object):

    # 链接数据库
    def __init__(self):
        try:
            config = {
                'host': '47.95.202.15',
                'port': 3306,
                'user': 'crawerdb',
                'password': 'crawerdb123',
                'db': 'crawerdb',
                'charset': 'utf8',
            }
            self.__db = pymysql.connect(**config)
        except pymysql.OperationalError as e:
            time.sleep(3)  # 秒级
            logging.error(e)
            self.to_connected()

    def select_all_data(self, sql_statement):
        cursor = self.__db.cursor()
        cursor.execute(sql_statement)
        data = cursor.fetchall()
        if cursor:
            cursor.close()
        return data

    def select_one_data(self, sql_statement):
        cursor = self.__db.cursor()
        cursor.execute(sql_statement)
        data = cursor.fetchone()
        if cursor:
            cursor.close()
        return data

    def update_data(self, sql_statement):
        cursor = self.__db.cursor()
        cursor.execute(sql_statement)
        self.__db.commit()
        if cursor:
            cursor.close()
        return True

    def insert_data(self, sql_statement):
        cursor = self.__db.cursor()
        cursor.execute(sql_statement)
        self.__db.commit()
        if cursor:
            cursor.close()
        return True
    def truncateTable(self, sql_statement):
        cursor = self.__db.cursor()
        cursor.execute(sql_statement)
        if cursor:
            cursor.close()
        return True

    def insert_data_no(self, sql_statement):
        cursor = self.__db.cursor()
        cursor.execute(sql_statement)
        self.__db.commit()

    def insert_many_data(self, sql_statement, val):
        cursor = self.__db.cursor()
        cursor.executemany(sql_statement, val)
        self.__db.commit()
        if cursor:
            cursor.close()
        return True

    def db_close(self):
        self.__db.close()

    def rollback(self):
        self.__db.rollback()

