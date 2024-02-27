import mariadb
from pymongo import MongoClient

mongo_db = MongoClient("mongodb://root:example@mongo:27017")

mariadb_connection = mariadb.connect(
        user = "user",
        password = "password",
        host = "maria",
        port = 3306,
        database = "testdb"
    )
cursor = mariadb_connection.cursor()

def _create_tables_if_not_exists():
    create_table_query = """
        CREATE TABLE IF NOT EXISTS tUsuarios (
            id VARCHAR(255) PRIMARY KEY,
            password VARCHAR(255)
        )
        """
    cursor.execute(create_table_query)
    mariadb_connection.commit()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS tTareas (
        id VARCHAR(36) PRIMARY KEY,
        user_id VARCHAR(255),
        text VARCHAR(255),
        created VARCHAR(20),
        updated VARCHAR(20),
        checked BOOLEAN,
        important BOOLEAN,
        FOREIGN KEY (user_id) REFERENCES tUsuarios(id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    """
    cursor.execute(create_table_query)
    mariadb_connection.commit()
    
_create_tables_if_not_exists()