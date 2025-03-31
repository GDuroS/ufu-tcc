from OruData.Service.AbstractService import AbstractCrudServiceClass
from anvil import tables
import anvil.server

refeicao_service = AbstractCrudServiceClass("Refeicao")
meta_diaria_service = AbstractCrudServiceClass("MetaDiaria")
user_service = AbstractCrudServiceClass('Users', has_sequence=False)
profissional_service = AbstractCrudServiceClass('Profissional')
dieta_tarefa_service = AbstractCrudServiceClass("DietaTarefa", has_sequence=False)

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
                meta_diaria_service.save(meta.row_changes)
            for meta in changed:
                meta_diaria_service.update(meta.original_row, meta.row_changes)
            for meta in removed:
                meta_diaria_service._delete(meta.original_row)

    def _validate(self, plano, refeicoes, metas):
        error_builder = []
        if plano['inicio'] is None or plano['termino'] is None:
            error_builder.append('As datas de início e término do Plano Alimentar são obrigatórias.')
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
               if metas['removed']:
                   error_builder.append("Não é permitido remover metas!")
        else:
            if not refeicoes or not refeicoes['added']: # Se não informou refeições ou é uma lista vazia
                error_builder.append('Todo plano precisa ter pelo menos uma refeição informada.')
            if not metas or not metas['added']:
                error_builder.append('Todo plano precisa ter suas metas informadas.')
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
        # Lógica abaixo foi substituída por buscar o plano mais recente
        # planos_vigentes = self.app_tables.planoalimentar.search(
        #     self.order_by('inicio', ascending=False), self.order_by('Sequence', ascending=False),
        #     paciente=paciente,
        #     inicio=self.q.less_than_or_equal_to(momento_atual),
        #     termino=self.q.any_of(None, self.q.greater_than_or_equal_to(momento_atual))
        # )
        planos_vigentes = self.app_tables.planoalimentar.search(
            self.order_by('termino', ascending=False), self.order_by('inicio', ascending=False), self.order_by('Sequence', ascending=False),
            paciente=paciente
        )
        try:
            return planos_vigentes[0]
        except IndexError:
            return None
        except Exception as e:
            self.log_error(e)
            raise e

    def get_tarefa(self, plano):
        tarefas = self.app_tables.dietatarefa.search(
            self.order_by('status', ascending=False), self.order_by('finish', ascending=False), self.order_by('start', ascending=False),
            plano=plano
        )
        tarefa = None
        for tarefa in tarefas:
            if tarefa['status'] == 'ABORTED':
                continue
            return tarefa
        return tarefa

    def get_report_object(self, plano_seq, load_refeicoes, load_metas, for_download=False):
        from ..Entities import PlanoAlimentar
        vo = PlanoAlimentar(self.get_by_sequence(plano_seq))
        if load_refeicoes:
            vo.refeicoes
        if load_metas:
            vo.metas
        vo.dietas
        vo.lock_changes = True
        if for_download:
            from anvil.pdf import PDFRenderer
            return PDFRenderer(
                filename=f"PlanoAlimentar_{vo['paciente']['nome'].split()[0]}_{'{:%d-%m}'.format(vo['inicio'])}_{'{:%d-%m-%y}'.format(vo['termino'])}.pdf",
            ).render_form('Components.Dietas.PlanoAlimentarReport', background='white', foreground='black', plano_alimentar=vo)
        return vo
        
plano_alimentar_service = PlanoAlimentarService()

class PacienteService(AbstractCrudServiceClass):
    def __init__(self):
        super().__init__('Paciente')

    def _merge_plano_vigente(self, paciente, plano):
        if plano is None or plano.is_empty:
            return
        refeicoes, metas = plano.refeicoes.list_changes, plano.metas.list_changes
        if plano.is_new:
            plano['paciente'] = paciente
            plano_alimentar_service._save(plano.row_changes, refeicoes, metas)
        else:
            plano_alimentar_service._update(plano.original_row, plano.row_changes, refeicoes, metas)

    def _validate(self, paciente):
        if not paciente.get('Sequence'):
            semelhantes = self.app_tables.paciente.search(profissional=paciente['profissional'], cpf=paciente['cpf'])
            if len(semelhantes) > 0:
                raise Exception("Já existe um paciente cadastrado com este CPF!")

    @tables.in_transaction
    def save(self, paciente, plano_vigente=None):
        self._validate(paciente)
        saved = AbstractCrudServiceClass.save(self, paciente)
        self._merge_plano_vigente(saved, plano_vigente)
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


class DietaService(AbstractCrudServiceClass):
    default_on_link_multiple_action = "CASCADE"
    
    def __init__(self):
        super().__init__("Dieta")

    def registrar_tarefa(self, plano_seq, task):
        from datetime import datetime
        self.app_tables.dietatarefa.add_row(task_id=task.get_id(), start=datetime.now(), plano=plano_alimentar_service.get_by_sequence(plano_seq), status="STARTED")
        
dieta_service = DietaService()

class DietaRefeicaoService(AbstractCrudServiceClass):
    action_by_column_remap = {'alimento': "NO_ACTION"}
    
    def __init__(self):
        super().__init__("DietaRefeicao")
    
    @anvil.server.background_task
    def gerar_dieta(self, plano_seq, vigencia_dieta, renovacao_pesos):
        if self is None:
            self = DietaRefeicaoService()
        try:
            from pulp import LpProblem, LpMinimize, LpVariable, LpBinary, LpStatus, lpSum, value
            from datetime import timedelta, datetime
            from ..Enums import AlimentoClassificacaoEnum, AlimentoComposicaoEnum
            
            state = anvil.server.task_state

            self.log_progress(step=1, progress=0, message="Iniciando variáveis")
            persist_buffer = []
            
            # TODO: substituir tables por self assim que possível
            self.log_progress(step=1, progress=1, message="Iniciando variáveis: Buscando Alimentos")
            alimentos = self.app_tables.alimento.search()

            self.log_progress(step=1, progress=5, message="Iniciando variáveis: Buscando dados do Plano do Paciente")
            plano_alimentar = self.app_tables.planoalimentar.get(Sequence=plano_seq)
            self.log_progress(step=1, progress=6)
            refeicoes = self.app_tables.refeicao.search(plano=plano_alimentar)
            self.log_progress(step=1, progress=8)
            metas_plano = self.app_tables.metadiaria.search(plano=plano_alimentar)
            
            self.log_progress(step=1, progress=9, message="Iniciando variáveis: Atualizando dados do Plano do Paciente")
            plano_alimentar.update(validade_dieta=vigencia_dieta, renovar_pesos=renovacao_pesos or None)
            self.log_progress(step=1, progress=10)

            self.log_progress(step=2, progress=10, message="Contando períodos a ajustar.")
            qtd_periodos = round((plano_alimentar['termino'] - plano_alimentar['inicio']) / timedelta(days=vigencia_dieta))
            pesos = {}
            curr_date = plano_alimentar['inicio']
            reset_pesos_when = curr_date
            
            def calcular_percentual_geral(percentual_local) -> int:
                """Calcula o percentual da tarefa de forma geral com base no percentual do progresso de cada loop"""
                periodos_completos = (curr_date - plano_alimentar['inicio']) // timedelta(days=vigencia_dieta)
                percentual_periodo_completo = 85.0 / qtd_periodos
                return (periodos_completos * percentual_periodo_completo) + (percentual_periodo_completo * percentual_local / 100.0) + 10.0
            def get_message_geral(message_local) -> str:
                periodos_completos = (curr_date - plano_alimentar['inicio']) // timedelta(days=vigencia_dieta)
                return f"Cálculo de Dietas: [{periodos_completos+1}/{qtd_periodos}] {message_local}"

            self.log_progress(step=3)
            while curr_date <= plano_alimentar['termino']:
                self.log_progress(progress=calcular_percentual_geral(0), message=get_message_geral("Definindo Pesos"))
                if renovacao_pesos and curr_date >= reset_pesos_when:
                    if not pesos:
                        # TODO: Aqui os pesos devem iniciar usando os dados do questionário do paciente
                        pesos = dict([(alimento['Sequence'], 0) for alimento in alimentos])
                    else:
                        pesos = {k:0 for k in pesos}
                    while curr_date >= reset_pesos_when:
                        reset_pesos_when += timedelta(days=renovacao_pesos)
                elif not pesos:
                    pesos = dict([(alimento['Sequence'], 0) for alimento in alimentos])
                
                self.log_progress(progress=calcular_percentual_geral(1), message=get_message_geral("Criando Problema"))
                prob = LpProblem(f"Problema Dieta {'{:%d/%m}'.format(curr_date)}", LpMinimize)

                ### BLOCO ESTÁTICO: Usado para definir estaticamente 2 vegetais
                chosen_vars = {}
                for alimento in alimentos:
                    if AlimentoClassificacaoEnum.VEGETAL.key in alimento['grupos']:
                        chosen_vars[alimento['Sequence']] = LpVariable(f"Chosen_{alimento['Sequence']}", 0, 1, LpBinary)
                ###
                
                self.log_progress(progress=calcular_percentual_geral(2), message=get_message_geral("Definindo Seleções"))
                food_vars = LpVariable.dicts("Selecao", (
                    [refeicao['Sequence'] for refeicao in refeicoes], [alimento['Sequence'] for alimento in alimentos]
                ), 0, cat="Integer")

                self.log_progress(progress=calcular_percentual_geral(3), message=get_message_geral("Definindo Objetivo"))
                ### BLOCO ESTÁTICO: Usado para definir proporção de 70 / 30 entre carboidratos e energia (não sei o que significa)
                prob += lpSum([
                    ( 
                        (0.7 * (alimento['carboidrato'] * food_vars[refeicao['Sequence']][alimento['Sequence']])) + 
                        (0.3 * (alimento['energia'] * food_vars[refeicao['Sequence']][alimento['Sequence']]) ) 
                    ) for refeicao in refeicoes for alimento in alimentos
                ])
                ###

                self.log_progress(progress=calcular_percentual_geral(8.5), message=get_message_geral("Calculando Totais de Refeições"))
                for refeicao in refeicoes:
                    ref = refeicao['Sequence']
                    total = sum(refeicao['quantidades'].values())
                    prob += lpSum([
                        food_vars[ref][alimento['Sequence']] for alimento in alimentos
                    ]) == total, f"Total_{refeicao['nome'].replace(' ', '_')}"
                
                ### BLOCO ESTÁTICO: Usado para definir estaticamente 2 vegetais
                prob += lpSum(chosen_vars[f] for f in chosen_vars) == 2, "Exactly_2_V_Foods"
                ###

                ### BLOCO ESTÁTICO: Usado para definir algo para Almoço
                for f in chosen_vars:
                    # TODO: Ainda não sei como definir isto
                    prob += food_vars[refeicoes[2]['Sequence']][f] <= chosen_vars[f], f"Choose_{f}_If_ChosenVar_Is_1"
                ###

                self.log_progress(progress=calcular_percentual_geral(13), message=get_message_geral("Aplicando Preferências Alimentares"))
                # Pesos
                prob += lpSum([
                    pesos[alimento['Sequence']] * food_vars[refeicao['Sequence']][alimento['Sequence']]
                    for refeicao in refeicoes for alimento in alimentos
                ]) <= 5.0
                
                self.log_progress(progress=calcular_percentual_geral(19), message=get_message_geral("Aplicando Metas Definidas"))
                for meta in metas_plano:
                    composicao_enum = AlimentoComposicaoEnum.by_key(meta['composicao'])
                    if meta['minimo']:
                        prob += lpSum(
                            alimento[composicao_enum.column_name] * food_vars[refeicao['Sequence']][alimento['Sequence']] 
                            for refeicao in refeicoes for alimento in alimentos
                        ) >= meta['minimo'], f"{composicao_enum.nome}Minimo"
                    if meta['maximo']:
                        prob += lpSum(
                            alimento[composicao_enum.column_name] * food_vars[refeicao['Sequence']][alimento['Sequence']] 
                            for refeicao in refeicoes for alimento in alimentos
                        ) <= meta['maximo'], f"{composicao_enum.nome}Maximo"

                self.log_progress(progress=calcular_percentual_geral(72), message=get_message_geral("Aplicando Restrições de Grupos"))
                ### BLOCO ESTÁTICO: Restrições adicionais
                def in_classe_possivel(alimento_classes, classes_possiveis):
                    for classe in alimento_classes:
                        if classe in classes_possiveis:
                            return True
                    return False
                for refeicao in refeicoes:
                    for classificacao in refeicao['quantidades']:
                        if '/' in classificacao:
                            # TODO: Bloco inatingível com a implementação atual
                            classes_possiveis = classificacao.split("/")
                            if classificacao == "FRUTA/LEITE" or classificacao == "BEBIDA/SUCO":
                                prob += lpSum([
                                    food_vars[refeicao['Sequence']][alimento['Sequence']]
                                    for alimento in alimentos if in_classe_possivel(alimento['grupos'], classes_possiveis)
                                ]) == refeicao['quantidades'][classificacao], f"{refeicao['nome']}_{classificacao}_Exact"
                            else:
                                prob += lpSum([
                                    food_vars[refeicao['Sequence']][alimento['Sequence']]
                                    for alimento in alimentos if in_classe_possivel(alimento['grupos'], classes_possiveis)
                                ]) <= refeicao['quantidades'][classificacao], f"{refeicao['nome']}_{classificacao}_Max"
                        else:
                            prob += lpSum([
                                food_vars[refeicao['Sequence']][alimento['Sequence']] 
                                for alimento in alimentos if classificacao in alimento['grupos']
                            ]) == refeicao['quantidades'][classificacao], f"{refeicao['nome']}_{classificacao}_Exact"
                
                self.log_progress(progress=calcular_percentual_geral(84), message=get_message_geral("Solucionando problema (esta etapa pode demorar e aparentar ter parado)"))
                prob.solve()

                self.log_progress(progress=calcular_percentual_geral(98.0), message=get_message_geral("Bufferizando refeições"))
                dietas_cadastradas = []
                for refeicao in refeicoes:
                    for alimento in alimentos:
                        var_value = food_vars[refeicao['Sequence']][alimento['Sequence']].varValue
                        if var_value > 0:
                            dietas_cadastradas.append({'refeicao': refeicao, 'alimento': alimento, 'quantidade': round(var_value, 2)})

                self.log_progress(progress=calcular_percentual_geral(98.5), message=get_message_geral("Bufferizando sumário"))
                summary = {}
                for composicao in AlimentoComposicaoEnum.list():
                    final = lpSum(
                        alimento[composicao.column_name] * food_vars[refeicao['Sequence']][alimento['Sequence']].varValue 
                        for refeicao in refeicoes for alimento in alimentos
                    )
                    summary[composicao.key] = value(final)
                
                self.log_progress(progress=calcular_percentual_geral(98.7), message=get_message_geral("Bufferizando dieta"))
                inicio = curr_date
                curr_date = curr_date + timedelta(days=vigencia_dieta)
                persist_buffer.append({
                    'plano': plano_alimentar, 
                    'inicio': inicio.date(), 'termino': min(curr_date - timedelta(days=1), plano_alimentar['termino']).date(), 
                    'refeicoes': dietas_cadastradas, 'summary': summary, 'f_objetivo': value(prob.objective), 'prob_status': LpStatus[prob.status]
                })
                
                self.log_progress(progress=calcular_percentual_geral(99), message=get_message_geral("Calculando pesos utilizados"))
                if curr_date < plano_alimentar['termino'] and curr_date < reset_pesos_when:
                    for peso in pesos:
                        count = sum(food_vars[refeicao['Sequence']][peso].varValue for refeicao in refeicoes)
                        if count > 0:
                            pesos[peso] += count
                        elif pesos[peso] > 0:
                            pesos[peso] -= 1
            
            self.log_progress(step=3, progress=96, message="Cálculo de Dietas: Concluído")
            @tables.in_transaction
            def persist_objects(buffer):
                for dieta in buffer:
                    refeicoes_cadastradas = []
                    for refeicao in dieta['refeicoes']:
                        refeicoes_cadastradas.append(self.save(refeicao))
                    dieta['refeicoes'] = refeicoes_cadastradas
                    dieta_service.save(dieta)

            self.log_progress(step=4, progress=96, message="Salvando Dietas calculadas")
            persist_objects(persist_buffer)
        except Exception as e:
            self.log_progress(message=e)
        else:
            self.log_progress(step=5, progress=100, message="Processo concluído sem erros")
            state['status'] = 'COMPLETED'
        finally:
            task = self.app_tables.dietatarefa.get(task_id=anvil.server.context.background_task_id)
            task.update(status=state['status'], log=state['log'], finish=datetime.now())

dieta_refeicao_service = DietaRefeicaoService()