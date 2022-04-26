from flask import Flask,request,jsonify
from .config import DefaultConfig
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager

__all__=['create_app']

def create_app(confij=None,app_name=None):

    if app_name==None:
        app_name=DefaultConfig.PROJECT
    
    app=Flask(app_name,instance_relative_config=True)
    mdb= PyMongo()
    jwt = JWTManager()


    
    mdb.init_app(app,uri="")
    jwt.init_app(app)


