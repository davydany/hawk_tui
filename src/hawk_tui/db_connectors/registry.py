from hawk_tui.db_connectors.base import ConnectionType, BaseConnection
from hawk_tui.db_connectors.postgresql import PostgreSQLConnection
from hawk_tui.db_connectors.mysql import MySQLConnection
# from hawk_tui.db_connectors.kafka import KafkaConnection
from hawk_tui.db_connectors.redis import RedisConnection
from hawk_tui.db_connectors.elasticsearch import ElasticsearchConnection


class ConnectionRegistry(object):

    def __init__(self):
        self.registry = {}
    
    def register(self, conn_type:ConnectionType, conn:BaseConnection):
        self.registry[conn_type] = conn
    
    def get(self, conn_type:ConnectionType):
        return self.registry[conn_type]
    
    def get_all(self):
        return self.registry
    

CONNECTION_REGISTRY = ConnectionRegistry()

CONNECTION_REGISTRY.register(ConnectionType.POSTGRES, PostgreSQLConnection)
CONNECTION_REGISTRY.register(ConnectionType.MYSQL, MySQLConnection)
# CONNECTION_REGISTRY.register(ConnectionType.KAFKA, KafkaConnection)
CONNECTION_REGISTRY.register(ConnectionType.REDIS, RedisConnection)
CONNECTION_REGISTRY.register(ConnectionType.ELASTICSEARCH, ElasticsearchConnection)

def create_connection(conn_type:ConnectionType, host:str, port:int, username:str=None, password:str=None, database:str=None):
    '''
    Create a connection of the given type with the provided parameters.

    Args:
        conn_type (ConnectionType): The type of connection to create.
        host (str): The host of the database.
        port (int): The port of the database.
        username (str, optional): The username to connect to the database. Defaults to None.
        password (str, optional): The password to connect to the database. Defaults to None.
        database (str, optional): The database to connect to. Defaults to None.

    Returns:
        Connection: The connection object.
    '''
    return CONNECTION_REGISTRY.get(conn_type)\
        (host, port, username, password, database)