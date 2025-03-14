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
		'ENERGIA': {'nome': 'Energia'},
		'PROTEINA': {'nome': 'Proteína'},
		'CARBOIDRATO': {'nome': 'Carboidrato'},
		'FIBRA': {'nome': 'Fibra'},
		'CALCIO': {'nome': 'Cálcio'},
		'MAGNESIO': {'nome': 'Magnésio'},
		'FERRO': {'nome': 'Ferro'},
		'FOSFORO': {'nome': 'Fósforo'},
		'MANGANES': {'nome': 'Manganês'},
		'SODIO': {'nome': 'Sódio'},
		'ZINCO': {'nome': 'Zinco'},
		'LIPIDIOS': {'nome': 'Lipídios'}
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