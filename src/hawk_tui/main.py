import click
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static

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
    result = pg.connect(host, port, username, password, database)
    app = DBConnectorApp()
    app.update_content(result)
    app.run()

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
    # result = postgresql.connect(host, port, username, password, database)
    # app = DBConnectorApp()
    # app.update_content(result)
    # app.run()
    pass

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
    result = postgresql.connect(host, port, username, password, database)
    app = DBConnectorApp()
    app.update_content(result)
    app.run()

@hawk.command()
@click.option('--host', default='localhost', help='Database host')
@click.option('--port', default=5432, help='Database port')
@click.option('--username', prompt=True, help='Database username')
@click.option('--password', prompt=True, hide_input=True, help='Database password')
@click.option('--database', default='postgres', help='Database name')
def redis(host, port, username, password, database):
    '''
    Sets up TUI for Redis.
    '''
    result = postgresql.connect(host, port, username, password, database)
    app = DBConnectorApp()
    app.update_content(result)
    app.run()

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
    result = postgresql.connect(host, port, username, password, database)
    app = DBConnectorApp()
    app.update_content(result)
    app.run()

