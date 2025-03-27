import anvil.server
from ..Service import dieta_service, dieta_refeicao_service

@anvil.server.callable
def getDietaById(sequence:int):
    return dieta_service.get_by_sequence(sequence)

@anvil.server.callable
def getDietaFind(*args, **kwargs):
    return dieta_service.find(*args, **kwargs)

@anvil.server.callable(require_user=True)
def postDieta(plano):
    return dieta_service.save(plano)

@anvil.server.callable(require_user=True)
def putDieta(plano, changes):
    return dieta_service.update(plano, changes)

@anvil.server.callable(require_user=True)
def deleteDieta(plano):
    dieta_service.delete(plano)

@anvil.server.callable(require_user=True)
def postDietaGerar(plano_seq, vigencia_dieta, renovacao_pesos):
    task = anvil.server.launch_background_task('gerar_dieta', dieta_refeicao_service, plano_seq, vigencia_dieta, renovacao_pesos)
    dieta_service.registrar_tarefa(plano_seq, task)
    return task
    