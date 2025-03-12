from ._anvil_designer import RefeicaoEditRowTemplateTemplate
from anvil import *
from anvil.js import get_dom_node

from .....Enums import AlimentoClassificacaoEnum

class RefeicaoEditRowTemplate(RefeicaoEditRowTemplateTemplate):
    def __init__(self, **properties):
        from anvil.js import get_dom_node
        # Set Form properties and Data Bindings.
        self.quantidade_items = [
            {'classificacao': key, 'quantidade': properties['item']['quantidades'].get(key, 0) if properties['item']['quantidades'] else 0}
            for key in AlimentoClassificacaoEnum.key_list()
        ]
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        def refresh(**event_args):
            self.refresh_data_bindings()
        self.add_event_handler('x-refresh', refresh)
        self.edit_panel.visible = False # Inicialização em view_mode sempre

    @property
    def view_mode(self):
        try:
            return self.parent.tag.form.view_mode
        except Exception:
            return True

    @property
    def horario_refeicao(self):
        return "{:%H:%M}".format(self.item['horario'])

    def edit_row_icon_button_click(self, **event_args):
        get_dom_node(self).classList.add('edit-mode-row')
        self.edit_panel.visible = True

    def remove_row_icon_button_click(self, **event_args):
        self.parent.raise_event('x-remove-self', refeicao=self.item)

    def cancel_button_click(self, **event_args):
        """This method is called when the component is clicked."""
        self.item.reset_changes()

    def save_button_click(self, **event_args):
        """This method is called when the component is clicked."""
        classificacoes = self.classificacoes_data_panel.items
        self.item['quantidades'] = {item['classificao']:item['quantidade'] for item in classificacoes}
        
        self.edit_panel.visible = False
        get_dom_node(self).classList.remove('edit-mode-row')
        self.refresh_data_bindings()

    
