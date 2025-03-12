from ._anvil_designer import PacienteEditTemplate
from anvil import *
from anvil.js import get_dom_node

from anvil_extras.popover import popover
from OruData.CrudInterface import CrudInterface
from ....Entities import Paciente, Refeicao

class PacienteEdit(CrudInterface, PacienteEditTemplate):
    def __init__(self, routing_context, **properties):
        CrudInterface.__init__(self, Paciente, routing_context, mode_switch_component=self.mode_switch, **properties)
        self.set_toggleable_components([
            self.nome_completo_text_box,
            self.nascimento_date_picker,
            self.cpftext_box
        ])

        # Any code you write here will run before the form opens.
        popover(self.planos_title_tooltip_heading, 'Planos são conjuntos de refeições planejadas para o paciente durante um período no qual são vigentes', title='Planos de Refeições', placement='auto', trigger='hover click')
        self.refeicoes_edit_data_panel.items = self.item.plano_vigente.refeicoes
        self._prepare_grid_visibility()
        self.routing_context.raise_init_events()

    def _prepare_grid_visibility(self):
        def remove_refeicao(refeicao, **event_args):
            self.item.plano_vigente.refeicoes.remove(refeicao)
            self.refeicoes_edit_data_panel.items = self.item.plano_vigente.refeicoes
            self.on_query_changed()
        def update_view(edit_mode, **event_args):
            self.add_refeicao_button.visible = not edit_mode
        self.refeicoes_edit_data_panel.tag.form = self
        self.refeicoes_edit_data_panel.add_event_handler('x-remove-self', remove_refeicao)
        self.refeicoes_edit_data_panel.add_event_handler('x-update-view', update_view)
        self.refeicoes_edit_data_grid.tag.all_columns = [c for c in self.refeicoes_edit_data_grid.columns]
        self.refeicoes_edit_data_grid.tag.view_columns = [c for c in self.refeicoes_edit_data_grid.columns if c['data_key'] != 'buttons']

    def on_query_changed(self, **event_args):
        CrudInterface.on_query_changed(self, **event_args)
        self.refeicoes_edit_data_grid.auto_header = not self.view_mode
        self.add_refeicao_button.visible = not self.view_mode
        get_dom_node(self.refeicoes_edit_data_panel).classList.toggle('no-auto-header', self.view_mode)
        if self.view_mode:
            self.refeicoes_edit_data_grid.columns = self.refeicoes_edit_data_grid.tag.view_columns
        else:
            self.refeicoes_edit_data_grid.columns = self.refeicoes_edit_data_grid.tag.all_columns
        self.refeicoes_edit_data_panel.raise_event_on_children('x-refresh')

    def before_save(self):
        if self.item.is_new:
            from ....Commons import LocalCommons
            self.item.profissional = LocalCommons().profissional

    def add_refeicao_button_click(self, **event_args):
        """This method is called when the component is clicked."""
        self.item.plano_vigente.refeicoes.append(Refeicao())
        self.refeicoes_edit_data_panel.items = self.item.plano_vigente.refeicoes
        self.on_query_changed()
        self.add_refeicao_button.visible = False # Pois ficará visível ao rodar on_query_changed
