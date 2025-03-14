import anvil.server
from ..Service import meta_diaria_service

@anvil.server.callable
def getMetaDiariaById(sequence:int):
    return meta_diaria_service.get_by_sequence(sequence)

@anvil.server.callable
def getMetaDiariaFind(*args, **kwargs):
    return meta_diaria_service.find(*args, **kwargs)

@anvil.server.callable(require_user=True)
def postMetaDiaria(meta_diaria):
    return meta_diaria_service.save(meta_diaria)

@anvil.server.callable(require_user=True)
def putMetaDiaria(meta_diaria, changes):
    return meta_diaria_service.update(meta_diaria, changes)

@anvil.server.callable(require_user=True)
def deleteMetaDiaria(meta_diaria):
    meta_diaria_service.delete(meta_diaria)