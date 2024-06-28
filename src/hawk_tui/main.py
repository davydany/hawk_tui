import click
import traceback
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static

from hawk_tui.db_connectors.base import ConnectionType
from hawk_tui.db_connectors.registry import create_connection
from hawk_tui.tui.registry import get_tui

class DBConnectorApp(App):

    def __init__(self, connection):
        super().__init__()

        self.connection = connection


    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(id="content")
        yield Footer()

    def update_content(self, content: str):
        self.query_one("#content", Static).update(content)

@click.group()
def hawk():
    '''
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⡿⠿⠿⠛⠛⠛⠛⠻⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⣀⣀⣠⣤⡾⢿⣿⣿⠿⠟⠉⠉⠀⠀⣠⣴⣶⣖⠒⡤⠀⠠⢾⣿⣭⣭⣾⣛⣻⣿⣿⣿⣿⣯⣍⣛⡿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⢀⡴⠛⠉⢁⣀⠀⢤⡀⠹⣇⠀⠢⠂⠀⠤⣾⠹⣿⣷⣟⡴⠃⠀⣀⣼⣭⣟⠛⠯⠭⠼⠿⢿⣿⣿⣿⣿⣿⣯⣽⣻⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⢀⡟⠁⢀⠎⠁⠀⠀⠈⠉⠆⠻⣿⣶⣀⣀⠀⠈⠓⠶⠶⠋⢁⣰⣾⣿⣭⡷⢖⣚⣿⠂⠌⣛⣻⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⢸⠁⠀⠀⠀⠀⠀⠀⠐⠲⠶⢄⠈⢿⣿⣿⣿⣿⣿⣷⡾⠿⠿⢿⣿⣞⠳⠾⣷⣻⢿⣯⠽⠛⠛⠉⣹⣿⣿⣿⣿⣿⣿⣿⣿⣝⢦⠀⠀⠀⠀⠀⠀⠀⠀
    ⢸⠀⠀⢀⡠⠖⠛⠛⠛⠲⣄⡀⠑⠈⢿⣿⣿⣿⣿⣿⣿⣋⣩⠭⣒⣛⠭⡗⣶⠽⠛⠋⠉⠀⣀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡻⢧⡀⠀⠀⠀⠀⠀⠀
    ⠸⡀⡠⠊⠉⠐⠲⢤⡂⢀⠀⠙⢦⡀⣀⠙⣿⣿⣿⣿⣿⣷⣶⠁⣲⣮⣝⣺⠷⠆⠀⠀⠀⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣵⡀⠀⠀⠀⠀⠀
    ⠀⠑⠁⠀⠀⠀⠀⠀⠈⠓⠷⣤⣠⣙⠻⠀⢸⣿⣿⣿⣿⣿⣿⣦⣶⡞⠉⠀⠀⠀⠀⠀⠸⠿⠛⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢤⠤⠝⠲⢿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠁⠀⠀⠀⠀⠀⠴⠾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠳⠁⠄⠀⠘⢿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣬⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⡀⠀⠀⠀⣽⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢹⠀⠀⠀⠀⢹⣿⣿⣿⣷⡂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡆⠀⠀⠀⠘⣿⣿⡿⢟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡐⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡍⠀⠀⠀⠀⠀⣀⠤⠤⠤⠀⠒⠒⢤⡤⠴⠞⠛⠻⠿⠛⠛⠛⠛⠛⠛⠋⠙⣿⠏⢻⣻⣿⣿⣿⣿⣿⣿⣿⡇
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⡠⣶⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠙⠿⠻⢿⠿⠿⠿⡇
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡠⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    Hawk Terminal UI
    ----------------
    Hawk is a TUI to connect to various databases and datastores.

    
    '''
    pass

@hawk.command()
@click.option('--host', default='localhost', help='Database host')
@click.option('--port', default=5432, help='Database port')
@click.option('--username', prompt=True, help='Database username')
@click.option('--password', prompt=True, hide_input=True, help='Database password')
@click.option('--database', default='postgres', help='Database name')
def postgresql(host, port, username, password, database):
    '''
    Sets up TUI for PostgreSQL database
    '''
    try:
        connection = create_connection(
            ConnectionType.POSTGRES, 
            host, 
            port, 
            username, 
            password, 
            database
        )
    except Exception as e:
        traceback.print_exc()
        

@hawk.command()
@click.option('--host', default='localhost', help='Database host')
@click.option('--port', default=5432, help='Database port')
@click.option('--username', prompt=True, help='Database username')
@click.option('--password', prompt=True, hide_input=True, help='Database password')
@click.option('--database', default='postgres', help='Database name')
def mysql(host, port, username, password, database):
    '''
    Sets up TUI for MySQL database
    '''
    try:
        connection = create_connection(
            ConnectionType.MYSQL, 
            host, 
            port, 
            username, 
            password, 
            database
        )
    except Exception as e:
        traceback.print_exc()

@hawk.command()
@click.option('--host', default='localhost', help='Database host')
@click.option('--port', default=5432, help='Database port')
@click.option('--username', prompt=True, help='Database username')
@click.option('--password', prompt=True, hide_input=True, help='Database password')
@click.option('--database', default='postgres', help='Database name')
def kafka(host, port, username, password, database):
    '''
    Sets up TUI for Kafka.
    '''
    try:
        connection = create_connection(
            ConnectionType.KAFKA, 
            host, 
            port, 
            username, 
            password, 
            database
        )
    except Exception as e:
        traceback.print_exc()

@hawk.command()
@click.option('--host', default='localhost', help='Database host')
@click.option('--port', default=6379, help='Database port')
@click.option('--password', prompt=True, hide_input=True, help='Database password')
@click.option('--database', default='0', help='Database Number')
def redis(host, port, password, database):
    '''
    Sets up TUI for Redis.
    '''
    try:
        if password:
            connection = create_connection(
                ConnectionType.REDIS, 
                host, 
                port,
                password=password,
                database=database
            )
        else:
            connection = create_connection(
                ConnectionType.REDIS, 
                host, 
                port,
                database=database
            )
        tui = get_tui(ConnectionType.REDIS, connection)
        tui.run()

    except Exception as e:
        traceback.print_exc()

@hawk.command()
@click.option('--host', default='localhost', help='Database host')
@click.option('--port', default=5432, help='Database port')
@click.option('--username', prompt=True, help='Database username')
@click.option('--password', prompt=True, hide_input=True, help='Database password')
@click.option('--database', default='postgres', help='Database name')
def elasticsearch(host, port, username, password, database):
    '''
    Sets up TUI for Elasticsearch.
    '''
    try:
        connection = create_connection(
            ConnectionType.ELASTICSEARCH, 
            host, 
            port, 
            username, 
            password, 
            database
        )
    except Exception as e:
        traceback.print_exc()
