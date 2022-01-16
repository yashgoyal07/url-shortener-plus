import logging
from models.mysql_model import MysqlModel
from controllers.cache_controller import CacheController
from helpers.mysql_queries import create_slink, show_slink, find_long_link
from helpers.constants import SLINK_CACHE_KEY


class LinksController(object):
    def __init__(self):
        self.mysql_model_obj = MysqlModel()
        self.cache_controller = CacheController()

    def create_slink(self, slink, long_link, customer_id):
        try:
            self.mysql_model_obj.dml_query(query=create_slink, query_params=(slink, long_link, customer_id))
        except Exception as err:
            logging.error(f'error from create_slink occured due to {err}')
            raise

    def show_slink(self, customer_id):
        try:
            result = self.mysql_model_obj.dql_query(query=show_slink, query_params=(customer_id,))
            return result
        except Exception as err:
            logging.error(f'error from show_slink occurred due to {err}')
            raise

    def find_long_link(self, slink):
        try:
            result = self.mysql_model_obj.dql_query(query=find_long_link, query_params=(slink,))
            if result:
                return result[0].get("long_link")
        except Exception as err:
            logging.error(f'error from find_customer occurred due to {err}')
            raise

    def get_long_link(self, slink_id):
        try:
            slink_cache_key = SLINK_CACHE_KEY.format(slink_id=slink_id)
            result = self.cache_controller.get(slink_cache_key)
            return result
        except Exception as err:
            logging.error(f'error from get_long_link occurred due to {err}')
            raise

    def set_long_link(self, slink_id, long_link):
        try:
            slink_cache_key = SLINK_CACHE_KEY.format(slink_id=slink_id)
            self.cache_controller.set(slink_cache_key, value=long_link, ex=15 * 24 * 3600)
        except Exception as err:
            logging.error(f'error from set_long_link occurred due to {err}')
            raise
