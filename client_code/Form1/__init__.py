from ._anvil_designer import Form1Template
from anvil import *

from ..Enums import AlimentoGrupoEnum

class Form1(Form1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        for grupo in AlimentoGrupoEnum.list():
            self.flow_panel_1.add_component(Label(font_size=20, icon=grupo._icon, foreground=grupo._color))
