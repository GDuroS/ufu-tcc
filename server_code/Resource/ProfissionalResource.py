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
def postProfissional(profissional):
    return profissional_service.save(profissional)

@anvil.server.callable(require_user=True)
def putProfissional(profissional, changes):
    return profissional_service.update(profissional, changes)

@anvil.server.callable(require_user=True)
def deleteProfissional(profissional):
    profissional_service.delete(profissional)