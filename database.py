import mysql.connector

class ranking():
    def __init__(self):
        self.ranking = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ranking"
        )
        self.mycursor = self.ranking.cursor()
    
    def insertar(self, nombre, puntaje):
        sql = "INSERT INTO usuario (usuario, puntaje) VALUES (%s, %s)"
        val = (nombre, puntaje)
        self.mycursor.execute(sql, val)

        self.ranking.commit()
        print(self.mycursor.rowcount, "record inserted.")