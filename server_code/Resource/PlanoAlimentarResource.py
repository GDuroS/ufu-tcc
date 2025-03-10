import anvil.server
from ..Service import plano_alimentar_service

@anvil.server.callable
def getPlanoAlimentarById(sequence:int):
    return plano_alimentar_service.get_by_sequence(sequence)

@anvil.server.callable
def getPlanoAlimentarFind(*args, **kwargs):
    return plano_alimentar_service.find(*args, **kwargs)

@anvil.server.callable(require_user=True)
def postPlanoAlimentar(plano):
    return plano_alimentar_service.save(plano)

@anvil.server.callable(require_user=True)
def putPlanoAlimentar(plano, changes):
    return plano_alimentar_service.update(plano, changes)

@anvil.server.callable(require_user=True)
def deletePlanoAlimentar(plano):
    plano_alimentar_service.delete(plano)

#
@anvil.server.callable
def getPlanoAlimentarVigentePorPaciente(paciente):
    return plano_alimentar_service.get_vigente_por_paciente(paciente)