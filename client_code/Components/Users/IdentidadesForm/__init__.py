from ._anvil_designer import IdentidadesFormTemplate
from anvil import *

class IdentidadesForm(IdentidadesFormTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        # self.layout
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.layout.set_required_components([
            self.layout.fullname_text_box,
            self.layout.display_name_text_box,
            self.cpf_text_box
        ], 'identidadeValidationGroup')
        
        if self.layout.mode == 'INIT':
            def merge_item():
                from anvil import server, users
                logged_user = users.get_user()
                result = server.call('getUserByCPF', self.cpf_text_box.cpf)
                if any(filter(lambda u: u != logged_user, result)):
                    Notification('Já existe um usuário com este CPF.\nUtilize "Esqueci a senha" para recuperar sua senha antiga ou entre em contato caso acredite que seja um erro.', title="Usuário já existe", timeout=5).show()
                    return False
                self.layout.item.merge()
                return True
            def merge_profissional():
                self.layout.item.profissional.merge()
                return True
            def update_user():
                from ....Commons import LocalCommons
                LocalCommons()._logged_user = None
                LocalCommons()._set_logged_user()
            self.dados_profissionais_card.visible = False
            self.layout.set_steps_list([
                {'card': self.layout.identidades_card, 'validation': 'identidadeValidationGroup', 'callback': merge_item},
                {'card': self.dados_profissionais_card, 'callback': merge_profissional}
            ], update_user)
        else:
            self.cpf_text_box.read_only = True
        
