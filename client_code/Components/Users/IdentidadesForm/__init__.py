from ._anvil_designer import IdentidadesFormTemplate
from anvil import *

from ....Entities import ProfissionalUser

class IdentidadesForm(IdentidadesFormTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.layout.user_class = ProfissionalUser
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.layout.set_required_components([
            self.layout.fullname_text_box,
            self.layout.display_name_text_box,
            self.cpf_text_box
        ], 'identidadeValidationGroup')
        
        if self.layout.mode == 'INIT':
            def merge_item():
                self.layout.item.merge()
            def merge_profissional():
                self.layout.item.profissional.merge()
            def update_user():
                from ....Commons import LocalCommons
                LocalCommons()._logged_user = None
                LocalCommons()._set_logged_user()
            self.dados_profissionais_card.visible = False
            self.layout.set_steps_list([
                {'card': self.layout.identidades_card, 'validation': 'identidadeValidationGroup', 'callback': merge_item},
                {'card': self.dados_profissionais_card, 'callback': merge_profissional}
            ], update_user)

    @property
    def mode(self):
        return self.layout.mode

    @mode.setter
    def mode(self, mode):
        self.layout.mode = mode
        
