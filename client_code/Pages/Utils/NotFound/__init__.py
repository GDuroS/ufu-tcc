from ._anvil_designer import NotFoundTemplate
from anvil import *


class NotFound(NotFoundTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
