from enum import Enum


from hawk_tui.db_connectors import postgresql as pg
from hawk_tui.db_connectors import mysql as my
from hawk_tui.db_connectors import kafka as kf
from hawk_tui.db_connectors import redis as rd
from hawk_tui.db_connectors import elasticsearch as es


class ConnectionType(Enum):

    POSTGRES = 1
    MYSQL = 2
    KAFKA = 3
    REDIS = 4
    ELASTICSEARCH = 5

class BaseConnection(object):

    def __init__(self, host:str, port:int, username:str=None, password:str=None, database:str=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

        self.connection = self.connect()

    def is_connected(self):
        
        raise NotImplementedError
    
    def connect(self):
        
        raise NotImplementedError
    
    def close(self):

        raise NotImplementedError
    
    

class Connection(object):

    def __init__(host:str, port:int, conn_type:ConnectionType, username:str=None, password:str=None, topic:str=None, database:str=None):
        self.host = host
        self.port = port
        self.conn_type = conn_type
        self.username = username
        self.password = password
        self.topic = topic
        self.database = database

        self.connection = self.connect()

    def connect(self):

        if self.conn_type == ConnectionType.POSTGRES:
            return pg.connect(self.host, self.port, self.username, self.password, self.database)
        
        elif self.conn_type == ConnectionType.MYSQL:
            return my.connect(self.host, self.port, self.username, self.password, self.database)
        
        elif self.conn_type == ConnectionType.KAFKA:
            return kf.connect_as_producer(self.host, self.port, self.username, self.password, self.topic)
        
        elif self.conn_type == ConnectionType.REDIS:
            return rd.connect(self.host, self.port, self.username, self.password, self.database)
        
        elif self.conn_type == ConnectionType.ELASTICSEARCH:
            return es.connect(self.host, self.port, self.username, self.password, self.database)
        
        else:
            return "Invalid connection type"