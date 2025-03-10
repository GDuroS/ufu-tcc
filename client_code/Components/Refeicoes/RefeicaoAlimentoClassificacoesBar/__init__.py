from ._anvil_designer import RefeicaoAlimentoClassificacoesBarTemplate
from anvil import *
from anvil.js import get_dom_node

from ....Enums import AlimentoClassificacaoEnum

class RefeicaoAlimentoClassificacoesBar(RefeicaoAlimentoClassificacoesBarTemplate):
    def __init__(self, **properties):
        get_dom_node(self).classList.add('refeicao-bar-component')
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    @property
    def alimentos_refeicao(self):
        return self.item

    @alimentos_refeicao.setter
    def alimentos_refeicao(self, item):
        self.item = item
        self.update_alimentos()

    def update_alimentos(self):
        self.panel.clear()
        for key, enum in AlimentoClassificacaoEnum.items():
            quantidade = self.item.get(key, 0)
            if quantidade > 0:
                self.panel.add_component(Label(
                    spacing_above=None, spacing_below=None, 
                    text=f'x{quantidade}', font_size=20, bold=True, foreground=enum['color'], 
                    icon=enum['icon'], icon_align='left', tooltip=enum['nome'],
                    role='icon-outline' if enum.get('outlined', False) else ''
                ))
