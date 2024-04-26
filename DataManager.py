import mysql.connector

class DataManager:
    # Constructeur qui prend les paramètres de la connexion
    # Prend en paramètre tous les champs pour la future chaîne de connexion
    def __init__(self, host, login, password, databaseName):
        self.host = host
        self.login = login
        self.password = password
        self.databaseName = databaseName
        # La connexion
        self.connection = None

    # La méthode pour se connecter
    def Connect(self):
        try:
            self.connection = mysql.connector.connect(host=self.host, user=self.login, password=self.password, database=self.databaseName)
            print("Connecté à la base de données !")
        except:
            print("Échec de connexion à la base de données.")

    # La méthode pour se déconnecter
    def Disconnect(self):
        if self.connection != None:
            self.connection.close()