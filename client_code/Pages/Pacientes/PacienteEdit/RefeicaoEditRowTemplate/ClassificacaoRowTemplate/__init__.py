from ._anvil_designer import ClassificacaoRowTemplateTemplate
from anvil import *


class ClassificacaoRowTemplate(ClassificacaoRowTemplateTemplate):
    def __init__(self, **properties):
        from ......Enums import AlimentoClassificacaoEnum
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        # XTZZLU
        self.enum = AlimentoClassificacaoEnum.by_key(self.item['classificacao'])
        self.add_component(
            Label(spacing_above=None, spacing_below=None, text=self.enum['nome'], icon=self.enum['icon']),
            column="XTZZLU"
        )
