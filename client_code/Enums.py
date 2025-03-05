from OruData.Enum import BaseEnum, _build_all

class AlimentoGrupo(BaseEnum):
    """Grupos de alimentos (também chamado de classificação)"""
    __options__ = {
        'BEBIDA': {'nome': 'Bebidas', 'codigo': 'B'}, # Bebidas
        'SUCO': {'nome': 'Sucos', 'codigo': 'S'}, # Frutas e derivados
        'FRUTA': {'nome': 'Frutas', 'codigo': 'F'}, # Frutas e derivados
        'LEITE': {'nome': 'Leites e Derivados', 'codigo': 'L'}, # Leite e derivados
        'PAO': {'nome': 'Cereais Derivados', 'codigo': 'C1'}, # Cereais e derivados
        'CEREAL': {'nome': 'Cereais', 'codigo': 'C2'}, # Cereais e derivados
        'GRAO': {'nome': 'Grãos', 'codigo': 'G'}, # Leguminosas e derivados
        'VEGETAIS': {'nome': 'Vegetais', 'codigo': 'V'}, # Vegerais e derivados
        'PROTEINA': {'nome': 'Proteínas', 'codigo': 'P'}
    }