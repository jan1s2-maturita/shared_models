import redis
import json
class RedisConnector:
    def __init__(self, host, port, db, user, password):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.password = password
        self.connection = redis.Redis(host=self.host, port=self.port, db=self.db, username=self.user, password=self.password)
    def get_connection(self):
        return self.connection
    def create_instance(self, user_id, image_id):
        self.connection.sadd(user_id, image_id)
    def delete_instance(self, user_id, image_id):
        self.connection.srem(user_id, image_id)

