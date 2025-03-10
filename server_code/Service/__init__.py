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

class PlanoAlimentarService(AbstractCrudServiceClass):
    def __init__(self):
        super().__init__('PlanoAlimentar')

    def get_vigente_por_paciente(self, paciente):
        from datetime import datetime
        momento_atual = datetime.now()
        planos_vigentes = self.app_tables.planoalimentar.search(
            self.order_by('inicio', ascending=False), self.order_by('Sequence', ascending=False),
            paciente=paciente,
            inicio=self.q.less_than_or_equal_to(momento_atual),
            termino=self.q.any_of(None, self.q.greater_than_or_equal_to(momento_atual))
        )
        try:
            return planos_vigentes[0]
        except Exception as e:
            self.log_error(e)
            return None

user_service = AbstractCrudServiceClass('Users')
profissional_service = AbstractCrudServiceClass('Profissional')
paciente_service = PacienteService()
plano_alimentar_service = PlanoAlimentarService()
refeicao_service = AbstractCrudServiceClass("Refeicao")