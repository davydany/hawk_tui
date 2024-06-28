import sys

from textual.app import App
from textual.screen import Screen

from hawk_tui.base import Base
from hawk_tui.db_connectors.base import BaseConnection

class BaseTUIApp(Base, App):

    CSS_PATH = "style.tcss"
    
    BINDINGS = [
        ('q', 'quit_app', 'Quit App'),
        ('d', 'toggle_dark', 'Toggle Dark Mode')
    ]

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_quit_app(self) -> None:
        """An action to quit the UI."""
        sys.exit(0)

    def __init__(self, connection:BaseConnection):
        super().__init__()

        self.connection = connection

    def draw(self):

        raise NotImplementedError
    
class BaseTUIScreen(Base, Screen):

    pass
