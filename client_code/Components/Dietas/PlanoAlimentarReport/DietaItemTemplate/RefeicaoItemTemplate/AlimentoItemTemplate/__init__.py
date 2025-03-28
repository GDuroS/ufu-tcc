from ._anvil_designer import AlimentoItemTemplateTemplate
from anvil import *


class AlimentoItemTemplate(AlimentoItemTemplateTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.alimento_text.text = f"{self.quantidade}x {self.alimento['descricao']}"

    @property
    def quantidade(self):
        return self.item[1]

    @property
    def alimento(self):
        return self.item[0]