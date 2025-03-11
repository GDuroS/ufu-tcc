from ._anvil_designer import RefeicaoEditRowTemplateTemplate
from anvil import *


class RefeicaoEditRowTemplate(RefeicaoEditRowTemplateTemplate):
    def __init__(self, **properties):
        from anvil.js import get_dom_node
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        def refresh(**event_args):
            self.refresh_data_bindings()
        self.add_event_handler('x-refresh', refresh)
        get_dom_node(self.classificacoes_data_panel).classList.add("min-padding")

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
        from anvil.js import get_dom_node
        get_dom_node(self).classList.add('edit-mode-row')
        self.edit_panel.visible = True

    def remove_row_icon_button_click(self, **event_args):
        self.parent.raise_event('x-remove-self', refeicao=self.item)

    
