from OruData.Enum import BaseEnum, _build_all

class AlimentoGrupoEnum(BaseEnum):
    """Grupos de alimentos (também chamado de classificação)"""
    __options__ = {
        'BEBIDA': {'nome': 'Bebidas', 'codigo': 'B', 'icon': 'fa:glass-water', 'color': 'lightblue'}, # Bebidas
        'SUCO': {'nome': 'Sucos', 'codigo': 'S', 'icon': 'fa:blender', 'color': '#4cdeb3'}, # Frutas e derivados
        'FRUTA': {'nome': 'Frutas', 'codigo': 'F', 'icon': 'fa:apple-whole', 'color': '#DD1533'}, # Frutas e derivados
        'LEITE': {'nome': 'Leites e Derivados', 'codigo': 'L', 'icon': 'fa:bottle-droplet', 'color': '#FDFFF5'}, # Leite e derivados
        'PAO': {'nome': 'Cereais Derivados', 'codigo': 'C1', 'icon': 'fa:bread-slice', 'color': '#9A6E61'}, # Cereais e derivados
        'CEREAL': {'nome': 'Cereais', 'codigo': 'C2', 'icon': 'fa:wheat-awn', 'color': '#ffa500'}, # Cereais e derivados
        'GRAO': {'nome': 'Grãos', 'codigo': 'G', 'icon': 'fa:seedling', 'color': '#C0CBA1'}, # Leguminosas e derivados
        'VEGETAIS': {'nome': 'Vegetais', 'codigo': 'V', 'icon': 'fa:carrot', 'color': '#E9692C'}, # Vegerais e derivados
        'PROTEINA': {'nome': 'Proteínas', 'codigo': 'P', 'icon': 'fa:egg', 'color': '#CAA892'}
    }
    
    BEBIDA = None
    SUCO = None
    FRUTA = None
    LEITE = None
    PAO = None
    CEREAL = None
    GRAO = None
    VEGETAIS = None
    PROTEINA = None

_build_all(__name__)