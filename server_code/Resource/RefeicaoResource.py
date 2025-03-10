import anvil.server
from ..Service import refeicao_service

@anvil.server.callable
def getRefeicaoById(sequence:int):
    return refeicao_service.get_by_sequence(sequence)

@anvil.server.callable
def getRefeicaoFind(*args, **kwargs):
    return refeicao_service.find(*args, **kwargs)

@anvil.server.callable(require_user=True)
def postRefeicao(refeicao):
    return refeicao_service.save(refeicao)

@anvil.server.callable(require_user=True)
def putRefeicao(refeicao, changes):
    return refeicao_service.update(refeicao, changes)

@anvil.server.callable(require_user=True)
def deleteRefeicao(refeicao):
    refeicao_service.delete(refeicao)