from OruData.Enum import BaseEnum, _build_all

class AlimentoClassificacaoEnum(BaseEnum):
    """Classificação de alimentos"""
    __options__ = {
        'BEBIDA': {'nome': 'Bebidas', 'codigo': 'B', 'icon': 'fa:glass-water', 'color': 'darkblue'}, # Bebidas
        'SUCO': {'nome': 'Sucos', 'codigo': 'S', 'icon': 'fa:blender', 'color': '#4cdeb3'}, # Frutas e derivados
        'FRUTA': {'nome': 'Frutas', 'codigo': 'F', 'icon': 'fa:apple-whole', 'color': '#DD1533'}, # Frutas e derivados
        'LEITE': {'nome': 'Leites e Derivados', 'codigo': 'L', 'icon': 'fa:bottle-droplet', 'color': '#FDFFF5', 'outlined': True}, # Leite e derivados
        'PAO': {'nome': 'Cereais Derivados', 'codigo': 'C1', 'icon': 'fa:bread-slice', 'color': '#9A6E61'}, # Cereais e derivados
        'CEREAL': {'nome': 'Cereais', 'codigo': 'C2', 'icon': 'fa:wheat-awn', 'color': '#ffa500'}, # Cereais e derivados
        'GRAO': {'nome': 'Grãos', 'codigo': 'G', 'icon': 'fa:seedling', 'color': '#C0CBA1'}, # Leguminosas e derivados
        'VEGETAL': {'nome': 'Vegetais', 'codigo': 'V', 'icon': 'fa:carrot', 'color': '#E9692C'}, # Vegetais e derivados
        'PROTEINA': {'nome': 'Proteínas', 'codigo': 'P', 'icon': 'fa:egg', 'color': '#CAA892'}
    }
    
    BEBIDA = None
    SUCO = None
    FRUTA = None
    LEITE = None
    PAO = None
    CEREAL = None
    GRAO = None
    VEGETAL = None
    PROTEINA = None

class AlimentoComposicaoEnum(BaseEnum):
    __options__ = {
		'ENERGIA': {'nome': 'Energia', 'default_min': 1800.0, 'default_max': None},
		'PROTEINA': {'nome': 'Proteína', 'default_min': 75.0, 'default_max': None},
		'CARBOIDRATO': {'nome': 'Carboidrato', 'default_min': 202.5, 'default_max': None},
		'FIBRA': {'nome': 'Fibra', 'default_min': 30.0, 'default_max': None},
		'CALCIO': {'nome': 'Cálcio', 'default_min': 850.0, 'default_max': None},
		'MAGNESIO': {'nome': 'Magnésio', 'default_min': 400.0, 'default_max': None},
		'FERRO': {'nome': 'Ferro', 'default_min': 18.0, 'default_max': None},
		'FOSFORO': {'nome': 'Fósforo', 'default_min': 700.0, 'default_max': None},
		'MANGANES': {'nome': 'Manganês', 'default_min': None, 'default_max': None},
		'SODIO': {'nome': 'Sódio', 'default_min': None, 'default_max': 2000.0},
		'ZINCO': {'nome': 'Zinco', 'default_min': 15, 'default_max': None},
		'LIPIDIOS': {'nome': 'Lipídios', 'default_min': None, 'default_max': 60.0}
	}

    ENERGIA = None
    PROTEINA = None
    CARBOIDRATO = None
    FIBRA = None
    CALCIO = None
    MAGNESIO = None
    FERRO = None
    FOSFORO = None
    MANGANES = None
    SODIO = None
    ZINCO = None
    LIPIDIOS = None

    @property
    def column_name(self):
        return self.key.lower()

_build_all(__name__)