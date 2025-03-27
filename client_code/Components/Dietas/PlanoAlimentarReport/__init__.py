from ._anvil_designer import PlanoAlimentarReportTemplate
from anvil import *


class PlanoAlimentarReport(PlanoAlimentarReportTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    @property
    def plano_alimentar(self):
        return self.item
