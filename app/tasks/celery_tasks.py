import logging

from celery import Celery

from controllers.cache_controller import CacheController
from controllers.mysql_controller import MysqlController
from helpers.constants import SLINK_CACHE_KEY
from helpers.mysql_queries import create_slink
from helpers.mysql_queries import update_customer, create_customer

### Instantiate Celery ###
celery = Celery('simple_task', broker='amqp://rabbitmq')


@celery.task
def create_customer_background(cus_id, name, email, mobile, password):
    try:
        MysqlController().dml_query(query=create_customer, query_params=(cus_id, name, email, mobile, password))
    except Exception as err:
        logging.error(f'error from create_customer occurred due to {err}')
        raise


@celery.task
def update_customer_background(name, email, mobile, password, cus_id):
    try:
        MysqlController().dml_query(query=update_customer, query_params=(name, email, mobile, password, cus_id))
    except Exception as err:
        logging.error(f'error from update_customer occurred due to {err}')
        raise


@celery.task
def create_slink_background(slink, long_link, customer_id):
    try:
        MysqlController().dml_query(query=create_slink, query_params=(slink, long_link, customer_id))
        slink_cache_key = SLINK_CACHE_KEY.format(slink_id=slink)
        CacheController().set(slink_cache_key, value=long_link)
    except Exception as err:
        logging.error(f'error from create_slink occured due to {err}')
        raise
