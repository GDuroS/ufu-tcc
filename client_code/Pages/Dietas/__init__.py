from ._anvil_designer import DietasTemplate
from anvil import *
from anvil.designer import in_designer

from ...Commons import LocalCommons

class Dietas(DietasTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.paciente_autocomplete_resync_click()

    def paciente_autocomplete_resync_click(self, **event_args):
        if in_designer:
            pacientes = [{'nome': 'Nome Paciente'}]
        else:
            pacientes = LocalCommons().get_pacientes()
        self.paciente_autocomplete.datasource = pacientes

    
