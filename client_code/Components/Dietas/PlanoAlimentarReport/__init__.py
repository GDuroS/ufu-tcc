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

    @plano_alimentar.setter
    def plano_alimentar(self, plano):
        self.item = plano
        self.form_heading.text = f"Plano Alimentar de {self.item['paciente']['nome']}"
        self.form_sub_heading.text = f"{'{:%d/%m/%Y}'.format(self.item['inicio'])} à {'{:%d/%m/%Y}'.format(self.item['termino'])}"
        if self.item['observacoes']:
            self.observacoes_panel.visible = True
            self.observacoes_text.content = self.item['observacoes']
        else:
            self.observacoes_panel.visible = False
        if self.item.refeicoes is None:
            self.refeicoes_panel.visible = False
        else:
            self.refeicoes_panel.visible = True
            # TODO: Refeições painel
        if self.item.metas is None:
            self.metas_panel.visible = False
        else:
            self.metas_panel.visible = True
            # TODO: Metas painel
        self.dietas_repeating_panel.items = self.item.dietas
        
