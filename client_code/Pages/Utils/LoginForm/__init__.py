from ._anvil_designer import LoginFormTemplate
from anvil import *

class LoginForm(LoginFormTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    @property
    def after_login_callback(self):
        return self.layout.after_login_callback
