from OruData.Service.AbstractService import AbstractCrudServiceClass
from anvil import tables

refeicao_service = AbstractCrudServiceClass("Refeicao")
meta_service = AbstractCrudServiceClass("Meta")
user_service = AbstractCrudServiceClass('Users')
profissional_service = AbstractCrudServiceClass('Profissional')

class PlanoAlimentarService(AbstractCrudServiceClass):
    def __init__(self):
        super().__init__('PlanoAlimentar')

    def _merge_refeicoes(self, plano, refeicoes):
        if refeicoes is not None and plano is not None:
            added = refeicoes['added']
            removed = refeicoes['removed']
            changed = refeicoes['changed']
            for refeicao in added:
                refeicao['plano'] = plano
                refeicao_service.save(refeicao.row_changes)
            for refeicao in changed:
                refeicao_service.update(refeicao.original_row, refeicao.row_changes)
            for refeicao in removed:
                refeicao_service._delete(refeicao.original_row)

    def _merge_metas(self, plano, metas):
        if metas is not None and plano is not None:
            added = metas['added']
            removed = metas['removed']
            changed = metas['changed']
            for meta in added:
                meta['plano'] = plano
                meta_service.save(meta.row_changes)
            for meta in changed:
                meta_service.update(meta.original_row, meta.row_changes)
            for meta in removed:
                meta_service._delete(meta.original_row)

    def _validate(self, plano, refeicoes, metas):
        error_builder = []
        if plano['inicio'] is None:
            error_builder.append('A data de início do Plano Alimentar é obrigatória.')
        if plano.get('termino'):
            if plano['inicio'] > plano['termino']:
                error_builder.append('A data de término não pode ser anterior à data de início.')
        if plano.get('Sequence', None):
            if refeicoes:
               # Alterou refeicoes
               if refeicoes['removed'] and not refeicoes['added']:
                   # removeu e não adicionou: pode ser que não hajam mais refeições
                   refeicoes_db = self.app_tables.refeicao.search(plano=plano)
                   removed = list(map(lambda r: r.original_row, refeicoes['removed']))
                   if not any(filter(lambda r: r not in removed, refeicoes_db)):
                       error_builder.append("Um plano não pode ficar sem refeições vinculadas!")
            if metas:
               # Alterou metas
               pass
        else:
            if not refeicoes or not refeicoes['added']: # Se não informou refeições ou é uma lista vazia
                error_builder.append('Todo plano precisa ter pelo menos uma refeição informada.')
            # if not metas or not metas['added']:
            #     error_builder.append('Todo plano precisa ter pelo menos uma meta informada.')
        if plano['paciente'] is None:
            error_builder.append('Todo plano precisa ser vinculado à um paciente.')
        else:
            planos_paciente = self.app_tables.planoalimentar.search(self.order_by('inicio'), paciente=plano['paciente'])
            for plano_saved in planos_paciente:
                if plano_saved['Sequence'] == plano['Sequence']:
                    continue
                    
                from datetime import timedelta, datetime
                if plano_saved['termino'] is None:
                    if plano['inicio'] > plano_saved['inicio']:
                        plano_saved.update(termino=plano['inicio'] - timedelta(days=1))
                        continue
                    error_builder.append("Já existem planos salvos para estas datas")
                    break
                plano_termino = plano['termino'] or datetime(3000, 12, 31)
                if (
                    plano['inicio'] <= plano_saved['inicio'] <= plano_termino or
                    plano['inicio'] <= plano_saved['termino'] <= plano_termino or
                    plano_saved['inicio'] <= plano['inicio'] <= plano_saved['termino']
                ):
                    error_builder.append("Já existem planos salvos para estas datas")
                    break
        if error_builder:
            raise Exception('\n'.join(error_builder))
                        
    @tables.in_transaction
    def save(self, plano, refeicoes, metas):
        return self._save(plano, refeicoes, metas)

    def _save(self, plano, refeicoes, metas):
        self._validate(plano, refeicoes, metas)
        saved = AbstractCrudServiceClass.save(self, plano)
        self._merge_refeicoes(saved, refeicoes)
        self._merge_metas(saved, metas)
        return saved

    @tables.in_transaction
    def update(self, plano, changes, refeicoes=None, metas=None):
        return self._update(plano, changes, refeicoes, metas)

    def _update(self, plano, changes, refeicoes=None, metas=None):
        if changes:
            self._validate({**{k:plano[k] for k, _ in plano}, **changes}, refeicoes, metas)
            updated = AbstractCrudServiceClass.update(plano, changes)
        else:
            updated = plano
        self._merge_refeicoes(updated, refeicoes)
        self._merge_metas(updated, metas)
        return updated

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
plano_alimentar_service = PlanoAlimentarService()

class PacienteService(AbstractCrudServiceClass):
    def __init__(self):
        super().__init__('Paciente')

    def _merge_plano_vigente(self, paciente, plano):
        if plano is None:
            return
        refeicoes, metas = getattr(plano, 'refeicoes', None), getattr(plano, 'metas', None)
        print("-----")
        print('refeicoes: ', refeicoes)
        print('refeicoes_direct: ', plano.refeicoes)
        print('refeicoes_compare: ', refeicoes is plano.refeicoes, refeicoes == plano.refeicoes)
        print('refeicao[0]: ', refeicoes[0])
        print('refeicao_direct[0]: ', plano.refeicoes[0])
        print('refeicao[0] compare:', refeicoes[0] is plano.refeicoes[0], refeicoes[0] == plano.refeicoes[0])
        raise Exception("stopped")
        if plano.is_new:
            plano['paciente'] = paciente
            plano_alimentar_service._save(plano.row_changes, refeicoes, metas)
        else:
            plano_alimentar_service._update(plano.original_row, plano.row_changes, refeicoes, metas)

    @tables.in_transaction
    def save(self, paciente, plano_vigente=None):
        saved = AbstractCrudServiceClass.save(self, paciente)
        self._merge_plano_vigente(paciente, plano_vigente)
        return saved

    @tables.in_transaction
    def update(self, paciente, changes, plano_vigente=None):
        updated = AbstractCrudServiceClass.update(paciente, changes) if changes else paciente
        self._merge_plano_vigente(updated, plano_vigente)
        return updated

    def get_by_user(self, user=None):
        if user is None:
            from anvil import users
            user = users.get_user()
        profissionais = self.app_tables.profissional.search(user=user)
        return self.app_tables.paciente.search(profissional=self.q.any_of(*profissionais))

paciente_service = PacienteService()