from ._anvil_designer import DietaItemTemplateTemplate
from anvil import *
from .....Enums import AlimentoComposicaoEnum

class DietaItemTemplate(DietaItemTemplateTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.dieta = self.item

    @property
    def dieta(self):
        return self.item

    @dieta.setter
    def dieta(self, dieta):
        self.item = dieta
        self.periodo_inicio_text.text = "{:%d/%m/%Y}".format(self.item['inicio'])
        self.periodo_termino_text.text = "{:%d/%m/%Y}".format(self.item['termino'])
        
        refeicoes_dieta = {}
        for dieta_refeicao in self.item['refeicoes']:
            refeicao = dieta_refeicao['refeicao']
            item = refeicoes_dieta.get(refeicao['Sequence'])
            if not item:
                item = {'refeicao': refeicao, 'alimentos': []}
                refeicoes_dieta[refeicao['Sequence']] = item
            item['alimentos'].append((dieta_refeicao['alimento'], dieta_refeicao['quantidade']))
        self.refeicao_repeating_panel.items = refeicoes_dieta.values()
        self.summary_data_panel.items = [{'composicao': AlimentoComposicaoEnum.by_key(comp).nome, 'value': round(value, 2)} for comp, value in self.item['summary'].items()]
