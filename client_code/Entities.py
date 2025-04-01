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
    def planos_alimentares(self):
        try:
            return getattr(self, '_planos_alimentares')
        except AttributeError:
            self._planos_alimentares = PlanoAlimentar.from_search(anvil.server.call('getPlanoAlimentarFind', paciente=self.original_row))
            return self._planos_alimentares

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

    def criar_novo_plano(self):
        """Cria um novo plano alimentar baseado no atual"""
        from datetime import datetime, timedelta
        plano_vigente = getattr(self, '_plano_vigente', None)
        if not plano_vigente:
            self._plano_vigente = PlanoAlimentar({'inicio': datetime.now()})
            self._plano_vigente.metas = MetaDiaria.create_metas_padrao()
            return self._plano_vigente
        elif plano_vigente.is_empty:
            # cria as metas no plano
            self._plano_vigente['inicio'] = datetime.now()
            self._plano_vigente.metas = MetaDiaria.create_metas_padrao()
            return self._plano_vigente
        elif plano_vigente.is_new:
            return None # Não faz sentido
        
        changes = {k:plano_vigente.original_row[k] for k in plano_vigente._original_key_list}
        novo_plano = PlanoAlimentar(changes)
        novo_plano['inicio'] = self['termino'] + timedelta(days=1) if self['termino'] else datetime.now()
        novo_plano['termino'] = novo_plano['inicio'] + self['termino'] - self['inicio'] if self['termino'] else None
        
        refeicoes = []
        for refeicao in plano_vigente.refeicoes:
            if refeicao.is_new:
                refeicoes.append(refeicao)
                continue
            ref_changes = {k:refeicao.original_row[k] for k in refeicao._original_key_list}
            refeicoes.append(Refeicao(ref_changes))
        novo_plano.refeicoes = refeicoes

        metas = []
        for meta in plano_vigente.metas:
            meta_changes = {k:meta.original_row[k] for k in meta._original_key_list}
            metas.append(MetaDiaria(meta_changes))
        novo_plano.metas = metas
        
        self._old_plano = plano_vigente
        self._plano_vigente = novo_plano
        
        return self._plano_vigente

    def reset_changes(self):
        Entity.reset_changes(self)
        if getattr(self, '_plano_vigente', None):
            if self.plano_vigente.is_new and hasattr(self, '_old_plano'):
                novo_plano = self.plano_vigente
                self.plano_vigente = self._old_plano
                del novo_plano
            self.plano_vigente.reset_changes()

    def merge(self):
        if not self.was_changed:
            raise ValueError("Não permitido quando o item não foi alterado.")
        plano_vigente = getattr(self, '_plano_vigente', None)
        if plano_vigente.is_empty:
            plano_vigente = None
        if self.is_new:
            # if plano_vigente is None or plano_vigente.is_empty:
                # raise Exception("É necessário informar um Plano Alimentar.")
            return Paciente(anvil.server.call('postPaciente', self.row_changes, plano_vigente))
        else:
            return Paciente(anvil.server.call('putPaciente', self.original_row, self.row_changes, plano_vigente))

@anvil.server.portable_class
class PlanoAlimentar(Entity):
    paciente = EntityDescriptor(Paciente)
    refeicoes = ManagedRelationship('Refeicao', 'plano')
    metas = ManagedRelationship('MetaDiaria', 'plano')
    dietas = ManagedRelationship('Dieta', 'plano')

    @property
    def tarefa(self):
        try:
            return getattr(self, '_tarefa')
        except AttributeError:
            self._tarefa = anvil.server.call('getPlanoAlimentarTarefa', plano=self.original_row)
            return self._tarefa

    def reset_changes(self):
        Entity.reset_changes(self)
        if getattr(self, '_managed_refeicoes', None):
            self.refeicoes.reset_changes()
        if getattr(self, '_managed_metas', None):
            self.metas.reset_changes()

    def __str__(self):
        return f"Plano de {'{:%d/%m/%Y}'.format(self['inicio'])} à {'{:%d/%m/%Y}'.format(self['termino'])}"

    @property
    def was_changed(self):
        was_changed = super().was_changed
        if not was_changed:
            if getattr(self, '_managed_refeicoes', None):
                was_changed = self.refeicoes.has_changes
        if not was_changed:
            if getattr(self, '_managed_metas', None):
                was_changed = self.metas.has_changes
        return was_changed
        

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

@anvil.server.portable_class
class MetaDiaria(Entity):
    plano = EntityDescriptor(PlanoAlimentar)
    _composicao_enum = None

    @property
    def composicao_enum(self):
        if self._composicao_enum is None and self['composicao'] is not None:
            from .Enums import AlimentoComposicaoEnum
            self._composicao_enum = AlimentoComposicaoEnum.by_key(self['composicao'])
        return self._composicao_enum

    @composicao_enum.setter
    def composicao_enum(self, value):
        self._composicao_enum = value
        self['composicao'] = value.key

    @property
    def composicao_nome(self):
        return self.composicao_enum.nome

    def reset_to_default(self):
        if self.composicao_enum:
            self['minimo'] = self.composicao_enum['default_min']
            self['maximo'] = self.composicao_enum['default_max']

    @staticmethod
    def create_metas_padrao(plano=None):
        from .Enums import AlimentoComposicaoEnum
        metas = []
        for comp in AlimentoComposicaoEnum.list():
            if comp['default_min'] is None and comp['default_max'] is None:
                continue # ignora manganês
            meta = MetaDiaria({'composicao': comp.key, 'minimo': comp['default_min'], 'maximo': comp['default_max']})
            if plano:
                meta['plano'] = plano
            metas.append(meta)
        return metas

    def __serialize__(self, global_data):
        self._composicao_enum = None
        return self.__dict__

@anvil.server.portable_class
class Dieta(Entity):
    plano = EntityDescriptor(PlanoAlimentar)