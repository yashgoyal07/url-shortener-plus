from configs.mysql_config import *

create_customer = f"""INSERT INTO {MysqlConfig.USER_DATABASE}.{MysqlConfig.CUSTOMERS_TABLE} (customer_id, name, email, mobile, password) VALUES (%s, %s, %s, %s, sha1(%s))"""
create_user = f"""INSERT INTO {MysqlConfig.USER_DATABASE}.{MysqlConfig.CUSTOMERS_TABLE} (customer_id) VALUES (%s)"""
find_customer = f"""SELECT customer_id FROM {MysqlConfig.USER_DATABASE}.{MysqlConfig.CUSTOMERS_TABLE} WHERE email = %s and password = sha1(%s)"""
update_customer = f"""UPDATE {MysqlConfig.USER_DATABASE}.{MysqlConfig.CUSTOMERS_TABLE} SET name = %s, email = %s, mobile = %s, password = sha1(%s) WHERE customer_id = %s"""
create_slink = f"""INSERT INTO {MysqlConfig.USER_DATABASE}.{MysqlConfig.LINKS_TABLE} (slink, long_link, customer_id) VALUES (%s, %s, %s)"""
show_slink = f"""SELECT * FROM {MysqlConfig.USER_DATABASE}.{MysqlConfig.LINKS_TABLE} WHERE customer_id = %s"""
find_long_link = f"""SELECT long_link FROM {MysqlConfig.USER_DATABASE}.{MysqlConfig.LINKS_TABLE} WHERE slink = %s"""
check_customer = f"""SELECT customer_id FROM {MysqlConfig.USER_DATABASE}.{MysqlConfig.CUSTOMERS_TABLE} WHERE email = %s"""