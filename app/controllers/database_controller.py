from controllers.mysql_controller import MysqlController
from helpers.mysql_queries import create_db, create_customer_table, create_links_table, empty_customer_table, empty_links_table, drop_db
import logging

def DatabaseSetup(object):
    def __init__(self):
        self.mysql_controller_obj = MysqlController()
        
    def db_creation(self):
        try:
            self.mysql_controller_obj.ddl_query(query=create_db)
        except Exception as err:
            logging.error(f'error from db_creation occurred due to {err}')
            raise
    
    def db_setup(self):
        try:
            self.mysql_controller_obj.ddl_query(query=create_customer_table)
            self.mysql_controller_obj.ddl_query(query=create_links_table)
        except Exception as err:
            logging.error(f'error from db_setup occurred due to {err}')
            raise
    
    def db_empty(self):
        try:
            self.mysql_controller_obj.ddl_query(query=empty_customer_table)
            self.mysql_controller_obj.ddl_query(query=empty_links_table)
        except Exception as err:
            logging.error(f'error from db_empty occurred due to {err}')
            raise


    def db_delete(self):
        try:
            self.mysql_controller_obj.ddl_query(query=drop_db)
        except Exception as err:
            logging.error(f'error from db_delete occurred due to {err}')
            raise