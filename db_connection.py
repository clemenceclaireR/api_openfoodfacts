#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

PRODUCTS_LINK = "https://fr.openfoodfacts.org/cgi/search.pl?"

HOST = "localhost"
DATABASE = "openfoodfacts"

USER = "user"
PASSWORD = "off"

TABLES = {'Categories': (
    "CREATE TABLE IF NOT EXISTS Categories ("
    " id SMALLINT(6) unsigned NOT NULL AUTO_INCREMENT,"
    " name VARCHAR(100) NOT NULL,"
    " PRIMARY KEY(id),"
    " UNIQUE KEY name (name)"
    " ) ENGINE=InnoDB;"),

    'Products': (
    "CREATE TABLE IF NOT EXISTS Products ("
    " id INT unsigned NOT NULL AUTO_INCREMENT,"
    " name VARCHAR(100),"
    " id_category SMALLINT(6) unsigned NOT NULL,"
    " brands VARCHAR(100),"
    " nutriscore CHAR(1),"
    " link VARCHAR(150),"
    " store VARCHAR(100),"
    " PRIMARY KEY(id),"
    " UNIQUE KEY name (name),"
    " CONSTRAINT fk_categories_id FOREIGN KEY (id_category)"
    " REFERENCES Categories(id) ON DELETE CASCADE"
    " ) ENGINE=InnoDB;")}

