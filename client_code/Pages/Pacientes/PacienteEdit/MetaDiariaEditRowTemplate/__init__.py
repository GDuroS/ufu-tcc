from ._anvil_designer import MetaDiariaEditRowTemplateTemplate
from anvil import *
from anvil.js import get_dom_node

from OruData.Validations import Validatable

class MetaDiariaEditRowTemplate(Validatable, MetaDiariaEditRowTemplateTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        Validatable.__init__(self)
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        def refresh(**event_args):
            self.refresh_data_bindings()
        def has_meta():
            return (self.item['minimo'] or 0) + (self.item['maximo'] or 0)

        Validatable.set_required_attributes(self, [
            (has_meta, 'A composição deve ter pelo menos uma meta diária mínima ou máxima.')
        ], 'metaValidationGroup')
        
        self.add_event_handler('x-refresh', refresh)
        self._prepare_styles()

    def _prepare_styles(self):
        get_dom_node(self).classList.add('edit-mode-extra-row')
        self.edit_data_row_panel.visible = False # Inicialização em view_mode sempre
        for child in get_dom_node(self.edit_data_row_panel).children:
            if child.getAttribute('data-grid-col-id') in ['BQOTRM', 'NPYXUT']:
                child.style.paddingRight = '10px'
                child.style.paddingLeft = '10px'

    @property
    def view_mode(self):
        try:
            return self.parent.tag.form.view_mode
        except Exception:
            return True

    def edit_row_icon_button_click(self, **event_args):
        get_dom_node(self).classList.add('edit-mode-row')
        self.edit_data_row_panel.visible = True

    def reset_row_icon_button_click(self, **event_args):
        self.item.reset_to_default()
        self.refresh_data_bindings()

    def minimo_maximo_text_box_change(self, **event_args):
        """This method is called when the text in this component is edited."""
        value = event_args['sender'].text
        if value is None or value == '':
            value = 0
        if value < 0:
            value = 0
        event_args['sender'].text = value

    def cancel_row_icon_button_click(self, **event_args):
        self.edit_data_row_panel.visible = False
        get_dom_node(self).classList.remove('edit-mode-row')
        self.refresh_data_bindings()

    def save_row_icon_button_click(self, **event_args):
        if self.is_valid('metaValidationGroup'):
            self.item['minimo'] = self.minimo_text_box.text
            self.item['maximo'] = self.maximo_text_box.text
            self.cancel_row_icon_button_click()
