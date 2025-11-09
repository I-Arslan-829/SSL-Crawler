from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from django.conf import settings

class MongoDBConnection:
    _instance = None
    _client = None
    _database = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self.connect()
    
    def connect(self):
        try:
            mongo_settings = settings.MONGODB_SETTINGS
            connection_string = f"mongodb://{mongo_settings['HOST']}:{mongo_settings['PORT']}/"
            
            self._client = MongoClient(
                connection_string,
                connectTimeoutMS=30000,
                socketTimeoutMS=30000,
                serverSelectionTimeoutMS=5000,
            )
            
            # Test connection
            self._client.admin.command('ping')
            self._database = self._client[mongo_settings['DATABASE']]
            print(f"✅ MongoDB connected successfully to {mongo_settings['DATABASE']}")
            
        except ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            raise
    
    def get_database(self):
        """Returns the MongoDB database instance"""
        return self._database
    
    def get_collection(self, collection_name):
        """Returns a specific MongoDB collection"""
        return self._database[collection_name]
    
    def close(self):
        """Close MongoDB connection"""
        if self._client:
            self._client.close()
            print("MongoDB connection closed")

# Global instance
mongodb = MongoDBConnection()
