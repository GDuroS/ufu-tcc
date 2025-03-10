from ._anvil_designer import RefeicaoEditRowTemplateTemplate
from anvil import *


class RefeicaoEditRowTemplate(RefeicaoEditRowTemplateTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    @property
    def view_mode(self):
        try:
            pass
        except:
            pass

    @property
    def horario_refeicao(self):
        return "{:%H:%M}".format(self.item['horario'])
