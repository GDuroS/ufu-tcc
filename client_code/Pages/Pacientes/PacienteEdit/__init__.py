from ._anvil_designer import PacienteEditTemplate
from anvil import *
from anvil.js import get_dom_node

from anvil_extras.popover import popover
from OruData.CrudInterface import CrudInterface
from ....Entities import Paciente, Refeicao

class PacienteEdit(CrudInterface, PacienteEditTemplate):
    def __init__(self, routing_context, **properties):
        CrudInterface.__init__(self, Paciente, routing_context, mode_switch_component=self.mode_switch, **properties)
        # self.refeicoes_card.visible = False
        self.metas_card.visible = False
        # self.no_plano_text.visible = True
        self._prepare_grid_visibility()
        if self.has_sequence:
            if self.item.plano_vigente is not None:
                self.plano_vigente_panel.visible = True
                self.refeicoes_card.visible = True
                self.metas_card.visible = True
                self.no_plano_text.visible = False
                if self.item.plano_vigente['observacoes']:
                    self.plano_observacoes_quill.set_html(self.item.plano_vigente['observacoes'])
                else:
                    self.plano_observacoes_quill.visible = False
                self.refeicoes_edit_data_panel.items = self.item.plano_vigente.refeicoes
                
        self.set_toggleable_components([
            self.nome_completo_text_box,
            self.nascimento_date_picker,
            self.cpftext_box,
            self.plano_inicio_date_picker,
            self.plano_termino_date_picker,
            self.plano_observacoes_quill
        ])

        # Any code you write here will run before the form opens.
        self.set_required_components([
            self.nome_completo_text_box,
            self.cpftext_box,
            self.nascimento_date_picker
        ])

        self.set_required_components([
            (self.plano_inicio_date_picker, 'Vigência do Plano Alimentar'),
        ], 'planoVigenteValidationGroup')

        def has_refeicoes():
            return self.item.plano_vigente.refeicoes
        self.set_required_attributes([
            (has_refeicoes, 'É obrigatório informar pelo menos uma refeição para o Plano')
        ], 'planoVigenteValidationGroup')

        popover(self.planos_title_tooltip_heading, 'Planos são conjuntos de refeições planejadas para o paciente durante um período no qual são vigentes', title='Planos de Refeições', placement='auto', trigger='hover click')
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
        if self.view_mode and not self.item.is_new and self.item.plano_vigente:
            self.refeicoes_edit_data_panel.items = self.item.plano_vigente.refeicoes
            if self.item.plano_vigente['observacoes']:
                self.plano_observacoes_quill.set_html(self.item.plano_vigente['observacoes'])
            else:
                self.plano_observacoes_quill.visible = False
        elif not self.view_mode:
            self.plano_observacoes_quill.visible = True

    def is_valid(self):
        is_valid = super().is_valid()
        if is_valid and self.item.plano_vigente:
            is_valid = super().is_valid('planoVigenteValidationGroup')
        return is_valid

    def before_save(self):
        if self.item.is_new:
            from ....Commons import LocalCommons
            self.item.profissional = LocalCommons().profissional
        if self.item.plano_vigente is not None:
            self.item.plano_vigente['observacoes'] = self.plano_observacoes_quill.get_html()

    def add_refeicao_button_click(self, **event_args):
        """This method is called when the component is clicked."""
        self.item.plano_vigente.refeicoes.append(Refeicao())
        self.refeicoes_edit_data_panel.items = self.item.plano_vigente.refeicoes
        self.on_query_changed()
        self.add_refeicao_button.visible = False # Pois ficará visível ao rodar on_query_changed

    def show_planos_link_click(self, **event_args):
        """This method is called clicked"""
        pass

    def new_plano_button_click(self, **event_args):
        """This method is called when the component is clicked."""
        self.item.plano_vigente = self.item.plano_vigente.novo_plano()
        self.refeicoes_card.visible = True
        self.metas_card.visible = True
        self.plano_vigente_panel.visible = True
        self.refresh_data_bindings()
