from hawk_tui.base import Base

class ConnectionType(Enum):

    POSTGRES = 1
    MYSQL = 2
    KAFKA = 3
    REDIS = 4
    ELASTICSEARCH = 5

class BaseConnection(Base):

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
    
    
