from ._anvil_designer import IdentidadesFormTemplate
from anvil import *


class IdentidadesForm(IdentidadesFormTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.layout.set_required_components([
            self.layout.fullname_text_box,
            self.layout.display_name_text_box,
            self.cpf_text_box
        ], 'identidadeValidationGroup')
        
        if self.layout.mode == 'INIT':
            self.dados_profissionais_card.visible = False
        self.layout.set_steps_list([
            {'card': self.layout.identidades_card, 'validation': 'identidadeValidationGroup'},
            {'card': self.dados_profissionais_card}
        ])
