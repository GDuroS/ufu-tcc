from ._anvil_designer import IdentidadesFormTemplate
from anvil import *


class IdentidadesForm(IdentidadesFormTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    @property
    def mode(self):
        return self.user_identity_component.mode

    @mode.setter
    def mode(self, value):
        self.user_identity_component.mode = value
