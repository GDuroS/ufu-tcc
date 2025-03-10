from ._anvil_designer import AlimentoClassificacoesLegendaTemplate
from anvil import *
from anvil.js import get_dom_node

from ....Enums import AlimentoClassificacaoEnum


class AlimentoClassificacoesLegenda(AlimentoClassificacoesLegendaTemplate):
    def __init__(self, **properties):
        get_dom_node(self).classList.add("refeicao-legenda-component")
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.update_alimentos()

    def update_alimentos(self):
        self.panel.clear()
        for key, enum in AlimentoClassificacaoEnum.items():
            self.panel.add_component(
                Label(
                    spacing_above=None,
                    spacing_below=None,
                    text=enum['nome'],
                    font_size=20,
                    bold=True,
                    foreground=enum["color"],
                    icon=enum["icon"],
                    icon_align="left",
                    role="icon-outline" if enum.get("outlined", False) else "",
                )
            )

    @property
    def background_color(self):
        return self.background

    @background_color.setter
    def background_color(self, value):
        self.background = value
