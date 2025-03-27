from ._anvil_designer import PlanoAlimentarReportTemplate
from anvil import *


class PlanoAlimentarReport(PlanoAlimentarReportTemplate):
    def __init__(self, routing_context, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.plano_alimentar_report.plano_alimentar = routing_context.nav_context['vo']
