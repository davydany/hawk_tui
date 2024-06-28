from hawk_tui.base import Base
from hawk_tui.db_connectors.base import ConnectionType, BaseConnection
from hawk_tui.tui.base import BaseTUIApp
from hawk_tui.tui.redis import RedisTUIApp

class TUIRegistry(Base):

    def __init__(self):
        self.registry = {}

    def register(self, conn_type:ConnectionType, tui:BaseTUIApp):
        self.registry[conn_type] = tui

    def get(self, conn_type:ConnectionType):
        return self.registry[conn_type]
    
    def get_all(self):
        return self.registry
    
TUI_REGISTRY = TUIRegistry()

TUI_REGISTRY.register(ConnectionType.REDIS, RedisTUIApp)


def get_tui(conn_type:ConnectionType, connection:BaseConnection):
    return TUI_REGISTRY.get(conn_type)(connection)