from OruData.Service.AbstractService import AbstractCrudServiceClass
from anvil import tables
import anvil.server

refeicao_service = AbstractCrudServiceClass("Refeicao")
meta_diaria_service = AbstractCrudServiceClass("MetaDiaria")
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
        planos_vigentes = self.app_tables.planoalimentar.search(
            self.order_by('inicio', ascending=False), self.order_by('Sequence', ascending=False),
            paciente=paciente,
            inicio=self.q.less_than_or_equal_to(momento_atual),
            termino=self.q.any_of(None, self.q.greater_than_or_equal_to(momento_atual))
        )
        try:
            return planos_vigentes[0]
        except IndexError:
            return None
        except Exception as e:
            self.log_error(e)
            raise e
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

from anvil_extras.logging import TimerLogger

class DietaService(AbstractCrudServiceClass):
    def __init__(self):
        super().__init__("Dieta")
    
    @anvil.server.background_task
    def gerar_dieta(self, plano_seq, vigencia_dieta, renovacao_pesos):
        timer = TimerLogger("Task timer")
        timer.start("Starting")
        try:
            from pulp import LpProblem, LpMinimize, LpVariable, LpBinary, LpStatus, lpSum, value
            from ..Enums import AlimentoClassificacaoEnum, AlimentoComposicaoEnum
            # state = anvil.server.task_state

            @tables.in_transaction
            def start_process(plano_seq, vigencia_dieta, renovacao_pesos):
                timer.check("start_process")
                
                # TODO: substituir tables por self assim que possível
                alimentos = tables.app_tables.alimento.search()
                timer.check("alimentos_search")

                plano_alimentar = tables.app_tables.planoalimentar.get(Sequence=plano_seq)
                refeicoes = tables.app_tables.refeicao.search(plano=plano_alimentar)
                metas_plano = tables.app_tables.metadiaria.search(plano=plano_alimentar)
                timer.check("plano_get+refeicoes+metas")
                
                plano_alimentar.update(validade_dieta=vigencia_dieta, renovar_pesos=renovacao_pesos)
                timer.check("plano_update")

                prob = LpProblem("Problema de Dieta Simples", LpMinimize)
                timer.check("prob init")

                ### BLOCO ESTÁTICO: Usado para definir estaticamente 2 vegetais
                chosen_vars = {}
                for alimento in alimentos:
                    if AlimentoClassificacaoEnum.VEGETAL.key in alimento['grupos']:
                        chosen_vars[alimento['Sequence']] = LpVariable(f"Chosen_{alimento['Sequence']}", 0, 1, LpBinary)
                ###
                timer.check('chosen_vars')
                
                food_vars = LpVariable.dicts("Selecao", (
                    [refeicao['Sequence'] for refeicao in refeicoes], [alimento['Sequence'] for alimento in alimentos]
                ), 0, cat="Integer")
                timer.check("food_vars")

                ### BLOCO ESTÁTICO: Usado para definir proporção de 70 / 30 entre carboidratos e energia (não sei o que significa)
                prob += lpSum([
                    ( 
                        (0.7 * (alimento['carboidrato'] * food_vars[refeicao['Sequence']][alimento['Sequence']])) + 
                        (0.3 * (alimento['energia'] * food_vars[refeicao['Sequence']][alimento['Sequence']]) ) 
                    ) for refeicao in refeicoes for alimento in alimentos
                ])
                ###
                timer.check("0.7/0.3")

                for refeicao in refeicoes:
                    ref = refeicao['Sequence']
                    total = sum(refeicao['quantidades'].values())
                    prob += lpSum([
                        food_vars[ref][alimento['Sequence']] for alimento in alimentos
                    ]) == total, f"Total_{refeicao['nome'].replace(' ', '_')}"
                timer.check("totais refeicoes")
                ### BLOCO ESTÁTICO: Usado para definir estaticamente 2 vegetais
                prob += lpSum(chosen_vars[f] for f in chosen_vars) == 2, "Exactly_2_V_Foods"
                ###
                timer.check("Exactly_2_V_Foods")

                ### BLOCO ESTÁTICO: Usado para definir algo para Almoço
                for f in chosen_vars:
                    # TODO: Ainda não sei como definir isto
                    prob += food_vars[refeicoes[2]['Sequence']][f] <= chosen_vars[f], f"Choose_{f}_If_ChosenVar_Is_1"
                ###
                timer.check("Almoço")

                # Pesos
                # TODO: Ajuste de peso
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
                timer.check("min/max")

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
                timer.check("Grupos")
                ###

                prob.solve()
                timer.check("Solve")
                print(f"Status: {LpStatus[prob.status]}")

                for refeicao in refeicoes:
                    print("\n")
                    print(f"Alimentos para {refeicao['nome']}")
                    for alimento in alimentos:
                        var_value = food_vars[refeicao['Sequence']][alimento['Sequence']].varValue
                        if var_value > 0:
                            print(f"{alimento['descricao']} = {round(var_value, 2)}")

                print("\n")
                for composicao in AlimentoComposicaoEnum.list():
                    final = lpSum(
                        alimento[composicao.column_name] * food_vars[refeicao['Sequence']][alimento['Sequence']].varValue 
                        for refeicao in refeicoes for alimento in alimentos
                    )
                    print(f"{composicao.nome}: {value(final)}")
                print(f"Função Objetivo: {value(prob.objective)}")
                timer.check("finished process")
            timer.check("After defining/before start process")
            start_process(plano_seq, vigencia_dieta, renovacao_pesos)
        except Exception as e:
            self.log_error(e)
        else:
            pass
        finally:
            timer.end("Finished")