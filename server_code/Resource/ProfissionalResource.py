import anvil.server
from ..Service import profissional_service

@anvil.server.callable
def getProfissionalById(sequence:int):
    return profissional_service.get_by_sequence(sequence)

@anvil.server.callable
def getProfissionalByUser(user):
    return profissional_service.get(user=user)

@anvil.server.callable
def getProfissionalFind(*args, **kwargs):
    return profissional_service.find(*args, **kwargs)

@anvil.server.callable(require_user=True)
def postProfissional(profissional, pontuacoes=None):
    return profissional_service.save(profissional, pontuacoes)

@anvil.server.callable(require_user=True)
def putProfissional(profissional, changes, pontuacoes=None):
    return profissional_service.update(profissional, changes, pontuacoes)

@anvil.server.callable(require_user=True)
def deleteProfissional(profissional):
    profissional_service.delete(profissional)