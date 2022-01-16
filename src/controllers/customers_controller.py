from controllers.mysql_controller import MysqlController
from helpers.mysql_queries import create_customer, update_customer, create_user, find_customer, check_customer
import logging


class CustomersController(object):
    def __init__(self):
        self.mysql_controller = MysqlController()

    def find_customer(self, email, password):
        try:
            result = self.mysql_controller.dql_query(query=find_customer, query_params=(email, password))
            return result
        except Exception as err:
            logging.error(f'error from find_customer occurred due to {err}')
            raise

    def create_user(self, cus_id):
        try:
            self.mysql_controller.dml_query(query=create_user, query_params=(cus_id,))
        except Exception as err:
            logging.error(f'error from create_user occurred due to {err}')
            raise

    def create_customer(self, cus_id, name, email, mobile, password):
        try:
            self.mysql_controller.dml_query(query=create_customer, query_params=(cus_id, name, email, mobile, password))
        except Exception as err:
            logging.error(f'error from create_customer occurred due to {err}')
            raise

    def update_customer(self, name, email, mobile, password, cus_id):
        try:
            self.mysql_controller.dml_query(query=update_customer, query_params=(name, email, mobile, password, cus_id))
        except Exception as err:
            logging.error(f'error from update_customer occurred due to {err}')
            raise

    def check_customer(self, email):
        try:
            result = self.mysql_controller.dql_query(query=check_customer, query_params=(email,))
            return result
        except Exception as err:
            logging.error(f'error from find_customer occurred due to {err}')
            raise