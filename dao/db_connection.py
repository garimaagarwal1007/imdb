import time
import pymysql
from service_bll.imdb_config import config


class DAO(object):
    def __init__(self, attribute="Database"):
        connText = config.get(attribute, 'connection_string')
        self.connstring = connText.split(",")
        self.db = attribute

    def execute_query(self, query, conn_str=None):
        start = time.clock()
        rows = []
        cnxn = None
        if conn_str is None:  # check connection string is provided or not
            conn_str = self.connstring  # if connection string is not provided then use default connection string
        else:
            conn_str = conn_str.split(",")

        try:
            cnxn = pymysql.connect(user=conn_str[1], passwd=conn_str[2], host=conn_str[0],
                                   database=conn_str[3], autocommit=False)
            cursor = cnxn.cursor()
            if isinstance(query, list):
                for subquery in query:
                    cursor.execute(subquery.encode('utf-8'))
            else:
                cursor.execute(query.encode('utf-8'))
            cnxn.commit()
            rows = cursor.fetchall()
        except Exception as e:
            if cnxn:
                cnxn.rollback()
            raise e
        finally:
            if cnxn:
                cnxn.close()
        # RTLogger.debug("Query executed in " + str(time.clock() - start) + "seconds", None)
        return rows

    def execute_query_get_description(self, query, conn_str=None):
        start = time.clock()
        rows = []
        cnxn = None
        if conn_str is None:  # check connection string is provided or not
            conn_str = self.connstring  # if connection string is not provided then use default connection string
        else:
            conn_str = conn_str.split(",")

        try:
            cnxn = pymysql.connect(user=conn_str[1], passwd=conn_str[2], host=conn_str[0],
                                   database=conn_str[3], autocommit=False)
            cursor = cnxn.cursor()
            if isinstance(query, list):
                for subquery in query:
                    cursor.execute(subquery.encode('utf-8'))
            else:
                cursor.execute(query.encode('utf-8'))
            cnxn.commit()
            rows = cursor.fetchall()
            columns = [item[0] for item in cursor.description]
        except Exception as e:
            if cnxn:
                cnxn.rollback()
            raise e
        finally:
            if cnxn:
                cnxn.close()
        return [rows, columns]

    #  This command is used for Insert, Update and Delete operations which returns row count
    def execute_non_query(self, query, conn_str=None):
        start = time.clock()
        rows = 0
        cnxn = None
        if conn_str is None:  # check connection string is provided or not
            conn_str = self.connstring  # if connection string is not provided then use default connection string
        else:
            conn_str = conn_str.split(",")
        try:
            if query:
                cnxn = pymysql.connect(user=conn_str[1], passwd=conn_str[2], host=conn_str[0],
                                       database=conn_str[3], autocommit=False)
                cursor = cnxn.cursor()
                if isinstance(query, list):
                    for subquery in query:
                        if subquery.strip():
                            cursor.execute(subquery.encode('utf-8'))
                            rows = cursor.rowcount
                else:
                    cursor.execute(query.encode('utf-8'))
                    rows = cursor.rowcount
                cnxn.commit()
            else:
                pass
        except Exception as e:
            if cnxn:
                cnxn.rollback()
            raise e
        finally:
            if cnxn:
                cnxn.close()
        # RTLogger.debug("Query executed in " + str(time.clock() - start) + "seconds", None)

        return rows

    def execute_many_mysql(self, query, arguments, conn_str=None):
        cnxn = None
        try:
            if conn_str is None:  # check connection string is provided or not
                conn_str = self.connstring  # if connection string is not provided then use default connection string
            else:
                conn_str = conn_str.split(",")
            cnxn = pymysql.connect(user=conn_str[1], passwd=conn_str[2], host=conn_str[0],
                                   database=conn_str[3], autocommit=False)
            rows = 0
            if query:
                cursor = cnxn.cursor()
                # Logger.log("Query to be executed \n"+query)
                cursor.executemany(query, arguments)
                rows = cursor.rowcount
                cnxn.commit()
                rows = cursor.fetchall()
        except Exception as e:
            pass
            if cnxn:
                cnxn.rollback()
            raise e
        finally:
            if cnxn:
                cnxn.close()
        return rows
