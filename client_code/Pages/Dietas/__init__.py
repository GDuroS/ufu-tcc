from ._anvil_designer import DietasTemplate
from anvil import *
from anvil import server
from anvil.designer import in_designer

from OruData.Validations import Validatable
from ...Commons import LocalCommons

class Dietas(Validatable, DietasTemplate):
    def __init__(self, **properties):
        self.geracao_progress_indicator.dom_nodes['anvil-m3-progressindicator-linear'].classList.add('m3-thick-progressindicator')
        # Set Form properties and Data Bindings.
        self.task = None
        Validatable.__init__(self)
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.set_required_components([
            self.paciente_autocomplete,
            self.plano_dropdown_menu,
            self.vigencia_text_box,
            self.renovacao_text_box
        ])
        self.paciente_autocomplete_resync_click()

    @property
    def plano_gerado(self):
        return None

    def paciente_autocomplete_resync_click(self, **event_args):
        if in_designer:
            pacientes = [{'nome': 'Nome Paciente'}]
        else:
            pacientes = LocalCommons().get_pacientes()
        self.paciente_autocomplete.datasource = pacientes
        self.reset_plano_dieta()

    def reset_plano_dieta(self):
        self.create_panel.visible = self.paciente_autocomplete.selected_value is not None
        self.plano_dropdown_menu.selected_value = None
        self.plano_dropdown_menu.items = [(str(plano), plano) for plano in self.paciente_autocomplete.selected_value.planos_alimentares]
        if self.paciente_autocomplete.selected_value.planos_alimentares:
            self.plano_dropdown_menu.selected_value = self.paciente_autocomplete.selected_value.planos_alimentares[-1]
            self.plano_dropdown_menu.read_only = False
            self.plano_dropdown_menu.placeholder = ''
            # Valores default
            self.vigencia_text_box.text = 7
            self.renovacao_text_box.text = ""
        else:
            self.plano_dropdown_menu.read_only = True
            self.plano_dropdown_menu.placeholder = 'Primeiro crie um Plano Alimentar na tela de cadastro'
        self.plano_dropdown_menu_change()

    def paciente_autocomplete_change(self, **event_args):
        """This method is called when an item is selected"""
        self.reset_plano_dieta()

    def plano_dropdown_menu_change(self, **event_args):
        """This method is called when an item is selected"""
        plano = self.plano_dropdown_menu.selected_value
        if plano:
            tarefa = plano.tarefa
            self.vigencia_text_box.visible = True
            self.renovacao_text_box.visible = True
            self.vigencia_text_box.disabled = tarefa and tarefa['status'] in ['RUNNING', 'COMPLETED']
            self.renovacao_text_box.disabled = tarefa and tarefa['status'] in ['RUNNING', 'COMPLETED']
            if tarefa:
                self.vigencia_text_box.text = plano['validade_dieta']
                self.renovacao_text_box.text = plano['renovar_pesos']
            self.gerar_button.visible = not tarefa or tarefa['status'] == 'ABORTED'
            self.geracao_progress_indicator.visible = tarefa and tarefa['status'] != 'COMPLETED'
            self.ver_receita_button.visible = False
            self.show_log_button.visible = True
            self.tarefa_status_text.visible = False
            if tarefa:
                self.geracao_progress_indicator # Progress
                self.tarefa_status_text.visible = True
                if tarefa['status'] == 'COMPLETED':
                    self.tarefa_status_text.content = "A dieta para este Plano Alimentar já foi previamente gerada."
                    self.ver_receita_button.visible = True
                elif tarefa['status'] == 'RUNNING':
                    # TODO: Busca dos dados da tarefa dentro de um timer
                    pass
                elif tarefa['status'] == 'ABORTED':
                    self.tarefa_status_text.content = "A geração de dieta para este Plano foi abortada devido à um erro."
                    self.show_log_button.visible = True
                
        else:
            self.vigencia_text_box.visible = False
            self.vigencia_text_box.disabled = False
            self.renovacao_text_box.visible = False
            self.renovacao_text_box.disabled = False
            self.gerar_button.visible = False
            self.geracao_progress_indicator.visible = False
            self.tarefa_status_text.visible = False
            self.show_log_button.visible = False
            self.ver_receita_button.visible = False

    def gerar_button_click(self, **event_args):
        """This method is called when the component is clicked."""
        if self.is_valid():
            self.task = server.call(
                'postDietaGerar', self.plano_dropdown_menu.selected_value['Sequence'],
                self.vigencia_text_box.text, self.renovacao_text_box.text
            )
            Notification("Geração de dietas programada com sucesso! Acompanhe o processo abaixo.", title="Geração programada", style="success").show()
            self.task_check_timer_tick()

    def show_log_button_click(self, **event_args):
        """This method is called when the component is clicked."""
        pass

    def ver_receita_button_click(self, **event_args):
        """This method is called when the component is clicked."""
        if self.plano_gerado:
            from OruData.Routing import navigate
            navigate(
                path="/relatorios/plano/:id", params={"id": self.plano_gerado['Sequence']}, 
                query={"r": False, "m": False, "mode": "view"},
                nav_context={'vo': self.plano_gerado}
            )

    def task_check_timer_tick(self, **event_args):
        """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
        self.task_check_timer.interval = 0
        
        self.task_check_timer.interval = 3

    
