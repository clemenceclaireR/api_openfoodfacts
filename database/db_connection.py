#! usr/bin/env python3
# -*- Coding: UTF-8 -*-


class DatabaseInformation:
    """
    Constants necessary in order to use the database
    """

    HOST = "localhost"
    DATABASE = "openfoodfacts"

    USER = "user"
    PASSWORD = "off2019"

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
            " ) ENGINE=InnoDB;"),

        'Favorites': (
            "CREATE TABLE IF NOT EXISTS Favorites ("
            " id SMALLINT(6) unsigned NOT NULL AUTO_INCREMENT,"
            " name_source_product VARCHAR(100),"
            " nutriscore_source_product CHAR(1),"
            " name_alternative_product VARCHAR(100),"
            " nutriscore_alternative_product CHAR(1),"
            " PRIMARY KEY(id),"
            " CONSTRAINT fk_products_name FOREIGN KEY (name_source_product)"
            " REFERENCES Products(name) ON DELETE CASCADE,"
            " CONSTRAINT fk_products_name_alternative FOREIGN KEY (name_alternative_product)"
            " REFERENCES Products(name) ON DELETE CASCADE"
            " ) ENGINE=INNoDB;")
    }
