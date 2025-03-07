import anvil.server
from ..Service import paciente_service

@anvil.server.callable
def getPacienteById(sequence:int):
    return paciente_service.get_by_sequence(sequence)

@anvil.server.callable
def getPacienteFind(*args, **kwargs):
    return paciente_service.find(*args, **kwargs)

@anvil.server.callable(require_user=True)
def getPacienteByUser(user=None):
    return paciente_service.get_by_user(user)

@anvil.server.callable(require_user=True)
def postPaciente(paciente):
    return paciente_service.save(paciente)

@anvil.server.callable(require_user=True)
def putPaciente(paciente, changes):
    return paciente_service.update(paciente, changes)

@anvil.server.callable(require_user=True)
def deletePaciente(paciente):
    paciente_service.delete(paciente)