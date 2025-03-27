from ._anvil_designer import ReportsTemplate
from anvil import *
from anvil import server, media
from anvil.designer import in_designer

from OruData.Routing import navigate
from OruData.Validations import Validatable
from ...Commons import LocalCommons

class Reports(Validatable, ReportsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        Validatable.__init__(self)
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.set_required_components([
            self.paciente_autocomplete,
            self.planos_dropdown_menu
        ], 'planoReportValidationGroup')
        
        self.options_select_box_panel.items = [
            ('Exibir parâmetros de Refeições', 'load_refeicoes'),
            ('Exibir parâmetros de Metas Diárias', 'load_metas'),
            ('Emitir para download', 'for_download')
        ]
        self.paciente_autocomplete_resync_click()

    def paciente_autocomplete_resync_click(self, **event_args):
        if in_designer:
            pacientes = [{'nome': 'Nome Paciente'}]
        else:
            pacientes = LocalCommons().get_pacientes()
        self.paciente_autocomplete.clear_field()
        self.paciente_autocomplete.datasource = pacientes
        self.reset_planos()

    def emitir_button_click(self, **event_args):
        if not self.is_valid('planoReportValidationGroup'):
            return
        vo = server.call('getPlanoAlimentarReport', 1, 'load_refeicoes' in self.options_select_box_panel.selected_values, 'load_metas' in self.options_select_box_panel.selected_values, 'for_download' in self.options_select_box_panel.selected_values)
        if 'for_download' in self.options_select_box_panel.selected_values:
            media.download(vo)
        else:
            navigate(
                path="/relatorios/plano/:id", params={"id": 1}, 
                query={"r": False, "m": False, "mode": "view"},
                nav_context={'vo': vo}
            )

    def reset_planos(self):
        paciente = self.paciente_autocomplete.selected_value
        if paciente:
            self.planos_dropdown_menu.items = [
                (str(plano), plano) for plano in paciente.planos_alimentares
                if True # TODO: Adicionar condição de plano gerado
            ]
        else:
            self.planos_dropdown_menu.items = []
        self.planos_dropdown_menu.selected_value = None

    def paciente_autocomplete_change(self, **event_args):
        """This method is called when an item is selected"""
        self.reset_planos()

    def clear_icon_button_click(self, **event_args):
        self.paciente_autocomplete_resync_click()
        self.options_select_box_panel.selected_values = None
