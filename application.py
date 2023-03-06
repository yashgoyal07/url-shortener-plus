import logging

from app import create_app
from app.controllers.database_controller import DatabaseSetup
from app.controllers.mysql_controller import MysqlController


def init_db():
    database_setup_obj = DatabaseSetup()
    database_setup_obj.db_creation()
    database_setup_obj.db_setup()


application = create_app()

if __name__ == '__main__':
    mysql_controller_obj = MysqlController()
    connection = None
    while not connection:
        try:
            logging.info(f"Retrying...")
            connection = mysql_controller_obj.get_connection()
        except Exception as err:
            logging.error(f"Connection not successfully Created")
    init_db()
    application.run(host='0.0.0.0', port=5000, debug=True)
