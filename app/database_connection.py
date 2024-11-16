import mysql.connector

class DatabaseConnection:
    def __init__(self, host="localhost", database="rdo_petro", user="root", password=""):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def connect(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return connection
        except mysql.connector.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None
