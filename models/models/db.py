from pymongo import MongoClient
from . import config
# Replace <mongodb_connection_string> with your MongoDB connection string
key = config.uri
client = MongoClient(key)

# Replace <database_name> with the name of your database
db = client.docs
