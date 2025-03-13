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

    @plano_vigente.setter
    def plano_vigente(self, plano):
        self._plano_vigente = PlanoAlimentar(plano)

    @property
    def was_changed(self):
        was_changed = super().was_changed
        if not was_changed:
            plano_vigente = getattr(self, '_plano_vigente', None)
            if plano_vigente:
                was_changed = plano_vigente.was_changed
        return was_changed

    def reset_changes(self):
        Entity.reset_changes(self)
        if getattr(self, '_plano_vigente', None):
            if self.plano_vigente.is_new:
                novo_plano = self.plano_vigente
                self.plano_vigente = self.plano_vigente._based_of
                del novo_plano
            else:
                self.plano_vigente.reset_changes()

    def merge(self):
        if not self.was_changed:
            raise ValueError("Não permitido quando o item não foi alterado.")
        plano_vigente = getattr(self, '_plano_vigente', None)
        if self.is_new:
            if plano_vigente is None:
                raise Exception("É necessário informar um Plano Alimentar.")
            return Paciente(anvil.server.call('postPaciente', self.row_changes, plano_vigente))
        else:
            return Paciente(anvil.server.call('putPaciente', self.original_row, self.row_changes, plano_vigente))

@anvil.server.portable_class
class PlanoAlimentar(Entity):
    _based_of = None
    paciente = EntityDescriptor(Paciente)
    refeicoes = ManagedRelationship('Refeicao', 'plano')

    def novo_plano(self):
        """Cria um novo plano alimentar baseado no atual"""
        from datetime import datetime, timedelta
        changes = {k:self.original_row[k] for k in self._original_key_list}
        novo_plano = PlanoAlimentar(changes)
        novo_plano['inicio'] = self['termino'] + timedelta(days=1) if self['termino'] else datetime.now().date()
        
        refeicoes = []
        for refeicao in self.refeicoes:
            if refeicao.is_new:
                refeicao['plano'] = novo_plano
                refeicoes.append(refeicao)
                continue
            ref_changes = {k:refeicao.original_row[k] for k in refeicao._original_key_list}
            ref_changes['plano'] = novo_plano
            refeicoes.append(Refeicao(ref_changes))
        novo_plano.refeicoes = refeicoes
        
        novo_plano._based_of = self
        return novo_plano

    def reset_changes(self):
        Entity.reset_changes(self)
        if getattr(self, '_managed_refeicoes', None):
            self.refeicoes.reset_changes()

    @property
    def was_changed(self):
        was_changed = super().was_changed
        if not was_changed:
            if getattr(self, '_managed_refeicoes', None):
                was_changed = self.refeicoes.has_changes
        return was_changed

    def __serialize__(self, global_data):
        self._based_of = None
        return self.__dict__

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
            self['horario'] = time_instance.isoformat(timespec='minutes')
        else:
            self['horario'] = None
    