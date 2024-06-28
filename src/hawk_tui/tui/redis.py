from textual import on
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Button, Footer, Header, DataTable, Select, Rule, TextArea
from textual.containers import Horizontal, Vertical, Grid, Container
from textual.reactive import Reactive
from textual.screen import Screen
from textual.widgets import Footer, Label, ListItem, ListView, Pretty, Input

from typing import List
from hawk_tui.base import Base
from hawk_tui.tui.base import BaseTUIApp, BaseTUIScreen
from hawk_tui.db_connectors.base import BaseConnection
from hawk_tui.db_connectors.redis import RedisConnection


class KeysListItem(ListItem):

    def __init__(self, key:int):
        super().__init__(Label(f"{key}"))
        self.key = key


# class AddKeyForm(BaseTUIScreen):

#     def __init__(self, connection: RedisConnection):

#         self.connection = connection
#         super().__init__()

#     def compose(self) -> ComposeResult:

#         yield Grid(
#             Label(id="lbl", placeholder="Add Key"),
#             Input(id="key", placeholder="Key:"),
#             Input(id="value", placeholder="Value:"),
#             Input(id="ttl", placeholder="TTL:"),
#             Button("Add", id="add-key"),
#             Button("Cancel", id="cancel"),
#         )

#     @on(Button.Pressed, "#add-key")
#     def add_key(self, event: Button.Pressed) -> None:

#         key = self.query_one("#key", Input).text
#         value = self.query_one("#value", Input).text
#         ttl = self.query_one("#ttl", Input).text

#         self.connection.set(key, value)
#         self.connection.expire(key, ttl)

#         self.app.pop_screen()

#     @on(Button.Pressed, "#cancel")
#     def cancel(self, event: Button.Pressed) -> None:
            
#         self.app.pop_screen()




class RedisTUIApp(BaseTUIApp):

    def update_ui(self):

        self.db_choices = [(f"Database {db}", db) for db in self.connection.list_databases()]

        self.db_columns = '\n'.join([f"DB {db}" for db in self.connection.list_databases()])
        self.key_columns = '\n'.join([f"{key} ({self.connection.connection.type(key)})" for key in self.connection.list_keys("*")])
        # self.value_column = f"Value: {self.key_info.get('value', 'N/A')}\n" \
        #                     f"TTL: {self.key_info.get('ttl', 'N/A')}\n" \
        #                     f"Info: {self.key_info.get('info', 'N/A')}"

    HEADERS = ['TYPE', 'KEY', 'VALUE', 'TTL', 'SIZE']

    ACTIVE_FILTER = "*"

    def compose(self) -> ComposeResult:

        self.update_ui()
        self.title = "Hawk TUI (Redis)"
        host = self.connection.host
        port = self.connection.port
        database = self.connection.database
        with_password = 'with password' if self.connection.password else 'without password'
        self.sub_title = f"Connected to redis://{host}:{port}/{database} {with_password}"

        yield Header()

        with Container(id="main_layout"):

            with Horizontal(id="controls_layout"):

                yield Button("❌  Delete Key", variant="primary", id="delete-key")
                yield Rule(orientation="vertical", line_style="heavy")
                yield Button("⬆️  Sort Ascending", variant="primary", id="sort-ascending")
                yield Rule(orientation="vertical", line_style="heavy")
                yield Button("⬇️  Sort Descending", variant="primary", id="sort-descending")
                yield Rule(orientation="vertical", line_style="heavy")
                yield Button("➕  Extend", variant="primary", id="extend")
                yield Rule(orientation="vertical", line_style="heavy")
                yield Button("🔄  Refresh", variant="primary", id="refresh")
                yield Rule(orientation="vertical", line_style="heavy")

            # with Horizontal(id="filter_layout"):
            #     yield Input(placeholder="Filter Keys", id="search", classes="text-input")
            #     yield Button("Filter", id="filter-button", classes="text-input")

            yield DataTable(id="data-table")

            yield TextArea()

        with Container(id="sidebar"):

            with Vertical(id="sidebar_layout"):

                yield Label("Add New Key")
                yield Input(placeholder="Key", id="key", classes="text-input")
                yield Input(placeholder="Value", id="value", classes="text-input")
                yield Input(placeholder="TTL", id="ttl", classes="text-input", type="integer")
                yield Button("Add Key", id="add-key", classes="text-input")

        yield Footer()

    # @on(Button.Pressed, "#add-key")
    # def add_key(self, event: Button.Pressed) -> None:
        
    #     form = AddKeyForm(self.connection)
    #     self.push_screen(form)

    def populate_rows(self) -> None:

        data_table = self.query_one(DataTable)
        keys = self.connection.list_keys(self.ACTIVE_FILTER)
        rows = []
        for key in keys:

            key_type = self.connection.type(key)
            key_value = self.connection.get(key)
            key_ttl = self.connection.ttl(key)
            key_size = self.connection.connection.memory_usage(key)
            rows.append([key_type, key, key_value, key_ttl, key_size])

        data_table.clear()
        data_table.add_rows(rows)

    def on_mount(self) -> None:

        self.update_ui()
        data_table = self.query_one(DataTable)
        data_table.add_columns(*self.HEADERS)
        self.populate_rows()
        
    def on_button_pressed(self, event: Button.Pressed) -> None:

        if event.button.id == "delete-key":
            pass
        elif event.button.id == "sort-ascending":
            pass
        elif event.button.id == "sort-descending":
            pass
        elif event.button.id == "extend":
            pass
        elif event.button.id == "refresh":
            
            data_table = self.query_one(DataTable)
            self.populate_rows()

        elif event.button.id == "add-key":
            
            key_field = self.query_one("#key", Input)
            key = key_field.value

            value_field = self.query_one("#value", Input)
            value = value_field.value
            
            ttl_field = self.query_one("#ttl", Input)
            ttl = ttl_field.value

            self.connection.set(key, value)
            self.connection.expire(key, ttl)
            
            key_field.value = ""
            value_field.value = ""
            ttl_field.value = ""


    
    def on_list_view_selected( self, event: ListView.Selected ) -> None: 
        """Called when the user click an item in the ListView.
        """
        
        log_view = self.query_one("#debug-info", Pretty)
        log_view.update(str(event.item.__dict__))


# class RedisTUIApp(BaseTUI, App):

#     databases: Reactive[List[int]] = Reactive([])
#     keys: Reactive[List[str]] = Reactive([])
#     selected_db: Reactive[int] = Reactive(0)
#     selected_key: Reactive[str] = Reactive("")
#     key_info: Reactive[dict] = Reactive({})
#     sort_ascending: Reactive[bool] = Reactive(True)

#     BINDINGS = [
#         ('q', 'quit_app', 'Quit App')
#     ]

#     def __init__(self, connection: RedisConnection):
#         BaseTUI.__init__(self, connection)
#         App.__init__(self)

#     def compose(self) -> ComposeResult:

        

#     # async def on_load(self) -> None:
#     #     """Bind keys here."""
#     #     await self.bind("q", "quit", "Quit")

#     # async def on_mount(self) -> None:
#     #     """Mount the widgets when the app starts."""
#     #     self.header = Header()
#     #     self.footer = Footer()
#     #     self.db_container = Container()
#     #     self.keys_container = Container()
#     #     self.value_container = Container()

#     #     self.refresh_data()

#     #     await self.view.dock(self.header, edge="top")
#     #     await self.view.dock(self.footer, edge="bottom")
#     #     await self.view.dock(self.db_container, edge="left", size=40)
#     #     await self.view.dock(self.keys_container, edge="center", size=40)
#     #     await self.view.dock(self.value_container, edge="right", size=60)

#     #     await self.update_ui()

#     def compose(self) -> ComposeResult:
#         self.header = Header()
#         self.footer = Footer()
#         self.db_container = Container()
#         self.keys_container = Container()
#         self.value_container = Container()

#         self.refresh_data()

#         yield self.header
#         yield self.db_container
#         yield self.keys_container
#         yield self.value_container
#         yield self.footer

#         yield self.update_ui()

#     def refresh_data(self):
#         self.databases = self.connection.list_databases()
#         self.update_keys()

#     def update_keys(self):
#         self.keys = self.connection.list_keys("*")
#         self.keys.sort(reverse=not self.sort_ascending)

#     async def update_ui(self):
#         db_column = "\n".join(
#             [f"DB {db}" for db in self.databases])
#         key_column = "\n".join(
#             [f"{key} ({self.connection.connection.type(key)})" for key in self.keys])
#         value_column = f"Value: {self.key_info.get('value', 'N/A')}\n" \
#                        f"TTL: {self.key_info.get('ttl', 'N/A')}\n" \
#                        f"Info: {self.key_info.get('info', 'N/A')}"

#         db_view = Static(db_column)
#         key_view = Static(key_column)
#         value_view = Static(value_column)

#         await self.db_container.update(db_view)
#         await self.keys_container.update(key_view)
#         await self.value_container.update(value_view)

#     async def action_quit(self) -> None:
#         """Exit the app."""
#         await self.shutdown()

#     async def on_click(self, event) -> None:
#         """Handle button press events."""
#         if isinstance(event, Button.Pressed):
#             button = event.button
#             if button.label == "Sort Ascending":
#                 self.sort_ascending = True
#                 self.update_keys()
#                 await self.update_ui()
#             elif button.label == "Sort Descending":
#                 self.sort_ascending = False
#                 self.update_keys()
#                 await self.update_ui()

#     def draw(self):
#         """Define the drawing logic for RedisTUI."""
#         self.refresh_data()
#         self.update_ui()
