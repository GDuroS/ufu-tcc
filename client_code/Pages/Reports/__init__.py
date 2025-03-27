from ._anvil_designer import ReportsTemplate
from anvil import *
from anvil import server

from OruData.Routing import navigate

class Reports(ReportsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def emitir_button_click(self, **event_args):
        vo = server.call('getPlanoAlimentarReport', 1, False, False)
        navigate(
            path="/relatorios/plano/:id", params={"id": 1}, 
            query={"r": False, "m": False, "mode": "view"},
            nav_context={'vo': vo}
        )
