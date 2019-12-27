#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

HOST = "localhost"
DATABASE = "openfoodfacts"

USER = "user"
PASSWORD = "off"

TABLES = {'Categories': (
    "CREATE TABLE IF NOT EXISTS Categories ("
    " id SMALLINT(6) unsigned NOT NULL AUTO_INCREMENT,"
    " name VARCHAR(200) NOT NULL,"
    " PRIMARY KEY(id),"
    " UNIQUE KEY name (name)"
    " ) ENGINE=InnoDB;"),

    'Products': (
    "CREATE TABLE IF NOT EXISTS Products ("
    " id INT unsigned NOT NULL AUTO_INCREMENT,"
    " id_category SMALLINT(6) unsigned NOT NULL,"
    " name VARCHAR(100),"
    " nutriscore CHAR(1),"
    " link VARCHAR(150),"
    " store VARCHAR(50),"
    " PRIMARY KEY(id),"
    " UNIQUE KEY name (name),"
    " CONSTRAINT fk_categories_id FOREIGN KEY (id_category)"
    " REFERENCES Categories(id) ON DELETE CASCADE"
    " ) ENGINE=InnoDB;")}

