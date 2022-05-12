from flask_pymongo import PyMongo
from rediscluster import RedisCluster
from flask_jwt_extended import JWTManager
from .config import DefaultConfig as Conf
import pyrebase 
firebase=pyrebase.initialize_app(Conf.FIREBASE_CONFIG)
auth=firebase.auth()

mdb = PyMongo()

print(Conf.REDIS_USERS_STARTUP_NODES)
redis_cluster = RedisCluster(
    startup_nodes=Conf.REDIS_USERS_STARTUP_NODES,
    decode_responses=True
)

print('Init Redis Cluster: successfully')
jwt = JWTManager()

