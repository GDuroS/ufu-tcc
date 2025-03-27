from ._anvil_designer import RefeicaoItemTemplateTemplate
from anvil import *


class RefeicaoItemTemplate(RefeicaoItemTemplateTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.dieta_refeicao = self.item

    @property
    def dieta_refeicao(self):
        return self.item

    @dieta_refeicao.setter
    def dieta_refeicao(self, refeicao):
        self.item = refeicao
        self.refeicao_heading.text = self.item['refeicao']['nome']
        self.refeicao_horario_text.text = self.item['refeicao']['horario']
        self.alimentos_repeating_panel.items = self.item['alimentos']
