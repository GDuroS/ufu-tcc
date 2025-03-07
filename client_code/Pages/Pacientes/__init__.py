from ._anvil_designer import PacientesTemplate
from anvil import *
from anvil.js import get_dom_node

from ...Commons import LocalCommons

class Pacientes(PacientesTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        get_dom_node(self.pacientes_data_panel).classList.add('grid-min-padding', 'main-list-grid')
        get_dom_node(self.filter_data_row_panel).classList.add('grid-min-padding', 'main-list-grid')
        
        self.refresh_pacientes()

    def refresh_pacientes(self):
        pacientes = LocalCommons().get_pacientes()
        self.pacientes_data_panel.items = pacientes
        self.paciente_summary_text.text = f"{len(pacientes)} pacientes cadastrados." if pacientes else "Nenhum paciente cadastrado"
