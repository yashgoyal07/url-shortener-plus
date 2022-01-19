from celery import Celery
from controllers.mysql_controller import MysqlController
from helpers.mysql_queries import update_customer
import logging

### Instantiate Celery ###
celery = Celery('simple_task', broker='amqp://localhost') 

@celery.task
def update_customer_background(name, email, mobile, password, cus_id):
    try:
        MysqlController().dml_query(query=update_customer, query_params=(name, email, mobile, password, cus_id))
    except Exception as err:
        logging.error(f'error from update_customer occurred due to {err}')
        raise