import anvil.server
from OruData.Entity import Entity, User, EntityDescriptor, ManagedRelationship

@anvil.server.portable_class
class ProfissionalUser(User):
    
    @classmethod
    def load_user(cls, buffer_changes=False):
        obj = super().load_user(buffer_changes)
        obj.profissional = Profissional.load_by_user(obj)
        return obj

@anvil.server.portable_class
class Profissional(Entity):
    user = EntityDescriptor(ProfissionalUser)

    @classmethod
    def load_by_user(cls, user):
        if isinstance(user, ProfissionalUser):
            user_obj = user
            user = user_obj.original_row
        else:
            user_obj = None
        obj = cls(anvil.server.call('getProfissionalByUser', user=user))
        if obj.is_new:
            obj['user'] = user
        if user_obj:
            obj._user_class = user_obj
        return obj

@anvil.server.portable_class
class Paciente(Entity):
    profissional = EntityDescriptor(Profissional)

    @property
    def plano_vigente(self):
        try:
            return getattr(self, '_plano_vigente')
        except AttributeError:
            self._plano_vigente = PlanoAlimentar(anvil.server.call('getPlanoAlimentarVigentePorPaciente', self.original_row))
            return self._plano_vigente

@anvil.server.portable_class
class PlanoAlimentar(Entity):
    paciente = EntityDescriptor(Paciente)
    refeicoes = ManagedRelationship('Refeicao', 'plano')

@anvil.server.portable_class
class Refeicao(Entity):
    plano = EntityDescriptor(PlanoAlimentar)

    @property
    def horario_time(self):
        if self['horario']:
            from datetime import time
            return time.fromisoformat(self['horario'])
        return None

    @horario_time.setter
    def horario_time(self, time_instance):
        if time_instance:
            self['horario'] = time_instance.isoformat()
        else:
            self['horario'] = None
    