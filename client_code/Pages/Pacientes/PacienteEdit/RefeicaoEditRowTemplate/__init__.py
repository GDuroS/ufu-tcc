from ._anvil_designer import RefeicaoEditRowTemplateTemplate
from anvil import *
from anvil.js import get_dom_node

class RefeicaoEditRowTemplate(RefeicaoEditRowTemplateTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

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

    
