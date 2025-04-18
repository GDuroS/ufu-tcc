from ._anvil_designer import RefeicaoEditRowTemplateTemplate
from anvil import *
from anvil.js import get_dom_node

from OruData.Validations import Validatable
from .....Enums import AlimentoClassificacaoEnum

class RefeicaoEditRowTemplate(Validatable, RefeicaoEditRowTemplateTemplate):
    def __init__(self, **properties):
        from anvil.js import get_dom_node
        # Set Form properties and Data Bindings.
        Validatable.__init__(self)
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        def refresh(**event_args):
            self.refresh_data_bindings()
        def total_quantidades():
            return sum(map(lambda c:c['quantidade'], self.classificacoes_data_panel.items))

        self.set_required_components([
            self.nome_edit_text_box,
            self.horario_edit_picker_component
        ], 'refeicaoValidationGroup')
        Validatable.set_required_attributes(self, [
            (total_quantidades, 'Pelo menos uma classificação deverá ter quantidades informadas.')
        ], 'refeicaoValidationGroup')
        
        self.add_event_handler('x-refresh', refresh)
        get_dom_node(self.classificacoes_data_panel).classList.add("min-padding")
        self.edit_panel.visible = False # Inicialização em view_mode sempre
        self.classificacoes_data_grid.remove_from_parent()

    @property
    def view_mode(self):
        try:
            return self.parent.tag.form.view_mode
        except Exception:
            return True

    @property
    def horario_refeicao(self):
        return "{:%H:%M}".format(self.item['horario'])

    @property
    def quantidade_items(self):
        return [
            {'classificacao': key, 'quantidade': self.item['quantidades'].get(key, 0) if self.item['quantidades'] else 0}
            for key in AlimentoClassificacaoEnum.key_list()
        ]

    def edit_row_icon_button_click(self, **event_args):
        get_dom_node(self).classList.add('edit-mode-row')
        self.classificacoes_data_panel.items = self.quantidade_items
        self.grid_container.add_component(self.classificacoes_data_grid)
        self.edit_panel.visible = True
        self.nome_edit_text_box.focus()
        self.parent.raise_event('x-update-view', edit_mode=True)

    def remove_row_icon_button_click(self, **event_args):
        self.parent.raise_event('x-remove-self', refeicao=self.item)

    def reset_view(self):
        self.edit_panel.visible = False
        self.classificacoes_data_grid.remove_from_parent()
        get_dom_node(self).classList.remove('edit-mode-row')
        self.parent.raise_event('x-update-view', edit_mode=False)
        self.refresh_data_bindings()
        self.edit_row_icon_button.scroll_into_view()

    def cancel_button_click(self, **event_args):
        """This method is called when the component is clicked."""
        if self.item.is_empty:
            self.remove_row_icon_button_click()
        else:
            self.reset_view()

    def save_button_click(self, **event_args):
        """This method is called when the component is clicked."""
        if self.is_valid('refeicaoValidationGroup'):
            self.item['nome'] = self.nome_edit_text_box.text
            self.item.horario_time = self.horario_edit_picker_component.time
            classificacoes = self.classificacoes_data_panel.items
            self.item['quantidades'] = {item['classificacao']:int(item['quantidade']) for item in classificacoes if item['quantidade'] is not None and item['quantidade'] > 0}
            self.reset_view()

    def form_show(self, **event_args):
        """This method is called when the form is shown on the page"""
        if self.item.is_empty:
            self.edit_row_icon_button_click()

    
