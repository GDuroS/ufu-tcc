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

    def reset_plano_dieta(self):
        self.plano_dropdown_menu.selected_value = None
        self.plano_dropdown_menu.items = []

    def paciente_autocomplete_change(self, **event_args):
        """This method is called when an item is selected"""
        self.create_button.visible = self.paciente_autocomplete.selected_value is not None
        self.create_panel.visible = False
        self.reset_plano_dieta()

    def create_button_click(self, **event_args):
        """This method is called when the component is clicked."""
        self.create_button.visible = False
        self.create_panel.visible = True
        self.plano_dropdown_menu.items = [(str(plano), plano) for plano in self.paciente_autocomplete.selected_value.planos_alimentares]
        self.plano_dropdown_menu.selected_value = self.paciente_autocomplete.selected_value.planos_alimentares[-1]

    
