from ._anvil_designer import MainLayoutTemplate
from anvil import *
from anvil.js import get_dom_node

from ...Commons import after_login_method

class MainLayout(MainLayoutTemplate):
    def __init__(self, **properties):
        # Changing styles
        self.main_card.dom_nodes['anvil-m3-card'].style.minHeight = '89vh'
        self.header_anchor.dom_nodes['anvil-m3-link'].classList.add('header-app-image')
        get_dom_node(self.header_panel).classList.add('hidden-when-mobile')
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        def hide_drawer(**event_args):
            self.layout.hide_nav_drawer()
        for link in self.nav_panel.get_components():
            link.add_event_handler('click', hide_drawer)

    @property
    def after_login_callback(self):
        return after_login_method
