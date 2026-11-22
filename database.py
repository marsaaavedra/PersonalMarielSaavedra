from pymongo import MongoClient
from pymongo.errors import PyMongoError
import certifi
import os

MONGO_URI = "mongodb+srv://marielsaavedra_db_user:losamobbs@cluster0.xrl9gq0.mongodb.net/"
ca = certifi.where()

def dbConnect():
    try:
        cliente = MongoClient(MONGO_URI, tlsCAFile=ca, serverSelectionTimeoutMS=5000)
        cliente.admin.command("ping")  # verifica que realmente conectó
        db = cliente["dbb_products_app"]
        return db
    except PyMongoError as e:
        print("Error de conexión a la base de datos:", e)
        return None

if __name__ == "__main__":
    db = dbConnect()
    if db is not None:
        print("Conectado a:", db.name)
    