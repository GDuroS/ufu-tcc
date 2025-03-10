from ._anvil_designer import LoginFormTemplate
from anvil import *


class LoginForm(LoginFormTemplate):
    def __init__(self, routing_context=None, **properties):
        # Set Form properties and Data Bindings.
        self.routing_context = routing_context
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    @property
    def login_callback(self):
        return self.layout.after_login_callback
