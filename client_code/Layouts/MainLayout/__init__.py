from ._anvil_designer import MainLayoutTemplate
from anvil import *

class MainLayout(MainLayoutTemplate):
    def __init__(self, **properties):
        # Changing styles
        self.main_card.dom_nodes['anvil-m3-card'].style.minHeight = '89vh'
        # self.header_panel.visible = False
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
