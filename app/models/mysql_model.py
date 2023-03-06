import logging

import mysql.connector

from configs.mysql_config import MysqlConfig
from helpers.utils import get_environment


class MysqlModel(object):
    def __init__(self):
        self.infra_env = get_environment()
        self.instance_config = MysqlConfig().INSTANCE_CONFIG.get(self.infra_env, {})

    def get_connection(self):
        try:
            connection = mysql.connector.connect(host=self.instance_config.get("host"),
                                                 port=self.instance_config.get("port"),
                                                 user=self.instance_config.get("username"),
                                                 password=self.instance_config.get("password"),
                                                 )
            return connection
        except mysql.connector.Error as e:
            raise Exception(f'mysql error occurred due to {e.msg}', e.errno)
        except Exception as err:
            logging.error(f'error from get_connection occurred due to {err}')
            raise

    def dml_query(self, query, query_params):
        connection = None
        try:
            connection = self.get_connection()
            cur = connection.cursor(dictionary=True)
            cur.execute(query, query_params)
            connection.commit()
            result = cur.rowcount
            return result
        except mysql.connector.Error as e:
            raise Exception(f'mysql error occurred due to {e.msg}', e.errno)
        except Exception as err:
            logging.error(f'error from dml_query occurred due to {err}')
            raise
        finally:
            if connection:
                connection.close()

    def dql_query(self, query, query_params=None):
        connection = None
        try:
            connection = self.get_connection()
            cur = connection.cursor(dictionary=True)
            if query_params:
                cur.execute(query, query_params)
            else:
                cur.execute(query)
            result = cur.fetchall()
            return result
        except mysql.connector.Error as e:
            raise Exception(f'mysql error occurred due to {e.msg}', e.errno)
        except Exception as err:
            logging.error(f'error from dql_query occurred due to {err}')
            raise
        finally:
            if connection:
                connection.close()

    def ddl_query(self, query):
        connection = None
        try:
            connection = self.get_connection()
            cur = connection.cursor()
            cur.execute(query)
        except mysql.connector.Error as e:
            raise Exception(f'mysql error occurred due to {e.msg}', e.errno)
        except Exception as err:
            logging.error(f'error from ddl_query occurred due to {err}')
            raise
        finally:
            if connection:
                connection.close()
