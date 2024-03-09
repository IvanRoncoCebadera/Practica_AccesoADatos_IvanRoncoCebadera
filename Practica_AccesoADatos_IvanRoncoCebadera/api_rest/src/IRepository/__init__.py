import mariadb
from pymongo import MongoClient
from dotenv import dotenv_values

ENV = dotenv_values()
print(ENV)

# MongoDB
user = ENV["MONGO_USER"]
password = ENV["MONGO_PWD"]
host = ENV["MONGO_HOST"]
port = ENV["MONGO_PORT"]
mongo_db = MongoClient(f"mongodb://{user}:{password}@{host}:{port}")

# MariaDB
mariadb_connection = mariadb.connect(
        user=ENV['MARIA_USER'],
        password=ENV['MARIA_PWD'],
        host=ENV['MARIA_HOST'],
        port=int(ENV['MARIA_PORT']),  # Asegúrate de convertir el puerto a entero
        database="testdb"
    )
cursor = mariadb_connection.cursor()

create_table_query = """
        CREATE TABLE IF NOT EXISTS tUsuarios (
            id VARCHAR(255) PRIMARY KEY,
            password VARCHAR(255)
        )
        """
cursor.execute(create_table_query)
mariadb_connection.commit()

create_table_query = """
    CREATE TABLE IF NOT EXISTS tListas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(255) NOT NULL,
        name VARCHAR(255),
        created VARCHAR(20),
        FOREIGN KEY (user_id) REFERENCES tUsuarios(id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    """
cursor.execute(create_table_query)
mariadb_connection.commit()

create_table_query = """
    CREATE TABLE IF NOT EXISTS tTareas (
        id VARCHAR(36) PRIMARY KEY,
        list_id INT NOT NULL,
        text VARCHAR(255),
        created VARCHAR(20),
        updated VARCHAR(20),
        checked BOOLEAN,
        important BOOLEAN,
        FOREIGN KEY (list_id) REFERENCES tListas(id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    """
cursor.execute(create_table_query)
mariadb_connection.commit()
