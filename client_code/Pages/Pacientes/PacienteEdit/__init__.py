from ._anvil_designer import PacienteEditTemplate
from anvil import *

from anvil_extras.popover import popover
from OruData.CrudInterface import CrudInterface
from ....Entities import Paciente

class PacienteEdit(CrudInterface, PacienteEditTemplate):
    def __init__(self, routing_context, **properties):
        CrudInterface.__init__(self, Paciente, routing_context, mode_switch_component=self.mode_switch, **properties)
        self.set_toggleable_components([
            self.nome_completo_text_box,
            self.nascimento_date_picker,
            self.cpftext_box
        ])

        # Any code you write here will run before the form opens.
        self._toggle_components()
        popover(self.planos_title_tooltip_heading, 'Planos são conjuntos de refeições planejadas para o paciente durante um período no qual são vigentes', title='Planos de Refeições', placement='auto', trigger='hover click')
        self.refeicoes_edit_data_panel.items = self.item.plano_vigente.refeicoes

    def before_save(self):
        if self.item.is_new:
            from ....Commons import LocalCommons
            self.item.profissional = LocalCommons().profissional
