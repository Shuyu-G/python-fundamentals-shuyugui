from mongoengine import connect

MONGO_USER = "appuser"
MONGO_PASS = "apppass"
MONGO_DB = "appdb"

connect(
    db=MONGO_DB,
    username=MONGO_USER,
    password=MONGO_PASS,
    host="mongodb://appuser:apppass@localhost:27017/appdb?authSource=appdb",
)
