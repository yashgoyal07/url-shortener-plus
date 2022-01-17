from configs.mysql_config import *

create_customer = f"""INSERT INTO {MysqlConfig.USER_DATABASE}.{MysqlConfig.CUSTOMERS_TABLE} (customer_id, name, email, mobile, password) VALUES (%s, %s, %s, %s, sha1(%s))"""
create_user = f"""INSERT INTO {MysqlConfig.USER_DATABASE}.{MysqlConfig.CUSTOMERS_TABLE} (customer_id) VALUES (%s)"""
find_customer = f"""SELECT customer_id FROM {MysqlConfig.USER_DATABASE}.{MysqlConfig.CUSTOMERS_TABLE} WHERE email = %s and password = sha1(%s)"""
update_customer = f"""UPDATE {MysqlConfig.USER_DATABASE}.{MysqlConfig.CUSTOMERS_TABLE} SET name = %s, email = %s, mobile = %s, password = sha1(%s) WHERE customer_id = %s"""
create_slink = f"""INSERT INTO {MysqlConfig.USER_DATABASE}.{MysqlConfig.LINKS_TABLE} (slink, long_link, customer_id) VALUES (%s, %s, %s)"""
show_slink = f"""SELECT * FROM {MysqlConfig.USER_DATABASE}.{MysqlConfig.LINKS_TABLE} WHERE customer_id = %s"""
find_long_link = f"""SELECT long_link FROM {MysqlConfig.USER_DATABASE}.{MysqlConfig.LINKS_TABLE} WHERE slink = %s"""
check_customer = f"""SELECT customer_id FROM {MysqlConfig.USER_DATABASE}.{MysqlConfig.CUSTOMERS_TABLE} WHERE email = %s"""


create_customer_table = f"""CREATE TABLE `url_shortener`.`customers` (
  `customer_id` VARCHAR(250) NOT NULL,
  `name` VARCHAR(250) NULL,
  `email` VARCHAR(250) NULL,
  `mobile` VARCHAR(250) NULL,
  `password` VARCHAR(250) NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE INDEX `customer_id_UNIQUE` (`customer_id` ASC) VISIBLE);"""

create_links_table = f"""CREATE TABLE `url_shortener`.`links` (
  `slink` VARCHAR(10) NOT NULL,
  `long_link` VARCHAR(700) NOT NULL,
  `customer_id` VARCHAR(250) NOT NULL,
  PRIMARY KEY (`slink`),
  UNIQUE INDEX `slink_UNIQUE` (`slink` ASC) VISIBLE);
"""