from OruData.Service.AbstractService import AbstractCrudServiceClass

class PacienteService(AbstractCrudServiceClass):
    def __init__(self):
        super().__init__('Paciente')

    def get_by_user(self, user=None):
        if user is None:
            from anvil import users
            user = users.get_user()
        profissionais = self.app_tables.profissional.search(user=user)
        return self.app_tables.paciente.search(profissional=self.q.any_of(*profissionais))

user_service = AbstractCrudServiceClass('Users')
profissional_service = AbstractCrudServiceClass('Profissional')
paciente_service = PacienteService()
plano_refeicao_service = AbstractCrudServiceClass("PlanoRefeicao")
refeicao_service = AbstractCrudServiceClass("Refeicao")