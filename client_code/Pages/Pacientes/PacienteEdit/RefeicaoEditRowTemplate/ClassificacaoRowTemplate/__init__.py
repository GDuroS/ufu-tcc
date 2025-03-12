from ._anvil_designer import ClassificacaoRowTemplateTemplate
from anvil import *


class ClassificacaoRowTemplate(ClassificacaoRowTemplateTemplate):
    def __init__(self, **properties):
        from ......Enums import AlimentoClassificacaoEnum
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        # XTZZLU
        self.enum = AlimentoClassificacaoEnum.by_key(self.item['classificacao'])
        self.add_component(
            Label(spacing_above=None, spacing_below=None, text=self.enum['nome'], bold=True, icon=self.enum['icon'], foreground='var(--anvil-m3-on-surface)' if self.enum.get('outlined', False) else self.enum['color']),
            column="XTZZLU"
        )

    def quantidade_text_box_change(self, **event_args):
        """This method is called when the text in this component is edited."""
        value = self.quantidade_text_box.text
        if value is None or value == '':
            value = 0
        if value < 0:
            value = 0
        self.quantidade_text_box.text = value
