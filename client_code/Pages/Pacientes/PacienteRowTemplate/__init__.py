from ._anvil_designer import PacienteRowTemplateTemplate
from anvil import *


class PacienteRowTemplate(PacienteRowTemplateTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    @property
    def nascimento_formatado(self):
        if self.item['nascimento']:
            return "{:%d/%m/%Y}".format(self.item['nascimento'])
        return None
