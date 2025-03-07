from ._anvil_designer import ErrorFormUnloggedTemplate
from anvil import *


class ErrorFormUnlogged(ErrorFormUnloggedTemplate):
    def __init__(self, routing_context, **properties):
        # Set Form properties and Data Bindings.
        self.routing_context = routing_context
        self.error_form.context
        print(f"{routing_context.error!r}")
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    @property
    def context(self):
        return self.routing_context
