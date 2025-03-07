from ._anvil_designer import PacientesTemplate
from anvil import *
from anvil.js import get_dom_node

from ...Commons import LocalCommons
import re

class Pacientes(PacientesTemplate):
    def __init__(self, **properties):
        self.date_pattern = re.compile(r'\D')
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

    def paciente_nome_filter_text_box_change(self, **event_args):
        """This method is called when the text in this component is edited."""
        pacientes = LocalCommons().get_pacientes()
        query = self.paciente_nome_filter_text_box.text
        self.pacientes_data_panel.items = [p for p in pacientes if not query or query in p['nome']]

    def paciente_nascimento_filter_text_box_change(self, **event_args):
        """This method is called when the text in this component is edited."""
        pacientes = LocalCommons().get_pacientes()
        query = self.date_pattern.sub('', self.paciente_nascimento_filter_text_box.text) if self.paciente_nascimento_filter_text_box.text else None
        self.pacientes_data_panel.items = [p for p in pacientes if not query or query in p['nascimento'].strftime('%d%m%Y')]
