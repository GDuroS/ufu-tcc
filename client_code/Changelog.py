from OruData.Enum import AbstractFuncionalidadeNotaEnum, TipoFuncionalidadeEnum, VersaoLevelEnum as LevelVersaoEnum

class FuncionalidadeNotaEnum(AbstractFuncionalidadeNotaEnum):
    __counter = 0

    def __init__(self, key:str, nome:str, descricao:str, level:LevelVersaoEnum, tipo:TipoFuncionalidadeEnum, component=None, route=None, important:bool=False, tutorial=None, service_worker_updated:bool=False, extra_params:dict=None):
        FuncionalidadeNotaEnum.__counter += 1
        key = key.replace(' ', '_').upper() if key is not None else f"FIX{str(FuncionalidadeNotaEnum.__counter).zfill(6)}"
        super().__init__(key, nome, descricao, level, self.get_app_id(), tipo, component, route, important, tutorial, service_worker_updated, extra_params)
        FuncionalidadeNotaEnum.__options__[key] = self

#Registro do Changelog (Deve ser registrado na ordem de RECENTES para ANTIGOS)
# ATENÇÃO: Tamanho máximo de chave deve acabar ->|