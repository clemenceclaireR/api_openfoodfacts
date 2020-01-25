CREATE TABLE Categories (
    id SMALLINT(6) unsigned NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY(id),
    UNIQUE KEY name (name)
    ) ENGINE=InnoDB;

CREATE TABLE Products (
    id INT unsigned NOT NULL AUTO_INCREMENT,
    name VARCHAR(100),
    id_category SMALLINT(6) unsigned NOT NULL,
    brands VARCHAR(100),
    nutriscore CHAR(1),
    link VARCHAR(150),
    store VARCHAR(100),
    PRIMARY KEY(id),
    UNIQUE KEY name (name),
    CONSTRAINT fk_categories_id FOREIGN KEY (id_category)
    REFERENCES Categories(id) ON DELETE CASCADE
    ) ENGINE=InnoDB;

CREATE TABLE Favorites (
    id SMALLINT(6) unsigned NOT NULL AUTO_INCREMENT,
    name_source_product VARCHAR(100),
    nutriscore_source_product CHAR(1),
    name_alternative_product VARCHAR(100),
    nutriscore_alternative_product CHAR(1),
    store_alternative_product VARCHAR(100),
    link_alternative_product VARCHAR(150),
    PRIMARY KEY(id),
    CONSTRAINT fk_products_name FOREIGN KEY (name_source_product)
    REFERENCES Products(name) ON DELETE CASCADE,
    CONSTRAINT fk_products_name_alternative FOREIGN KEY (name_alternative_product)
    REFERENCES Products(name) ON DELETE CASCADE
    ) ENGINE=INNoDB;



