class MysqlConfig(object):
    INSTANCE_CONFIG = {'local': {
        "host": "db",
        "port": 3306,
        "username": "root",
        "password": "admin"
    }, 'qa': {
        "host": "10.11.XX.XX",
        "port": 3306,
        "username": "root",
        "password": "########"
    }, 'prod': {
        "host": "10.11.XX.XX",
        "port": 3306,
        "username": "root",
        "password": "########"
    }}

    USER_DATABASE = "url_shortener"
    CUSTOMERS_TABLE = "customers"
    LINKS_TABLE = "links"
