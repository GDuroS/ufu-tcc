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
        self.vo = None
        Validatable.__init__(self)
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.set_required_components([
            self.paciente_autocomplete,
            self.plano_dropdown_menu,
            self.vigencia_text_box
        ])
        self.paciente_autocomplete_resync_click()

    @property
    def plano_gerado(self):
        return self.vo

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
        if self.paciente_autocomplete.selected_value:
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
            self.geracao_progress_indicator.visible = tarefa and tarefa['status'] == 'RUNNING'
            self.percentage_text.visible = self.geracao_progress_indicator.visible
            self.ver_receita_button.visible = False
            self.show_log_button.visible = False
            self.tarefa_status_text.visible = False
            self.tarefa_status_text.align = 'left'
            # self.tarefa_status_text.foreground = ''
            if tarefa:
                self.tarefa_status_text.visible = True
                self.vigencia_text_box.read_only = True
                self.renovacao_text_box.read_only = True
                if tarefa['status'] == 'COMPLETED':
                    self.tarefa_status_text.content = "**A dieta para este Plano Alimentar já foi previamente gerada.**"
                    self.tarefa_status_text.foreground = 'var(--anvil-m3-primary)'
                    self.ver_receita_button.visible = True
                elif tarefa['status'] == 'RUNNING':
                    self.task = server.call('getTaskById', tarefa['task_id'])
                    self.task_check_timer_tick()
                elif tarefa['status'] == 'ABORTED':
                    self.tarefa_status_text.content = "*A geração de dieta para este Plano foi abortada devido à um erro.*"
                    self.tarefa_status_text.foreground = 'var(--anvil-m3-tertiary)'
                    self.tarefa_status_text.align = 'center'
                    self.show_log_button.visible = True
                    self.vigencia_text_box.read_only = False
                    self.renovacao_text_box.read_only = False
        else:
            self.vigencia_text_box.visible = False
            self.vigencia_text_box.disabled = False
            self.renovacao_text_box.visible = False
            self.renovacao_text_box.disabled = False
            self.gerar_button.visible = False
            self.geracao_progress_indicator.visible = False
            self.percentage_text.visible = False
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
            self.geracao_progress_indicator.type = 'indeterminate'
            self.geracao_progress_indicator.visible = True
            self.geracao_progress_indicator.progress_color = ''
            self.percentage_text.visible = True
            self.gerar_button.visible = False
            self.show_log_button.visible = False
            self.vigencia_text_box.read_only = True
            self.renovacao_text_box.read_only = True
            Notification("Geração de dietas programada com sucesso! Acompanhe o processo abaixo.", title="Geração programada", style="success").show()
            self.task_check_timer_tick()

    def show_log_button_click(self, **event_args):
        """This method is called when the component is clicked."""
        from m3.components import TextArea as m3Area
        if not self.task:
            self.task = server.call('getTaskById', self.plano_dropdown_menu.selected_value.tarefa['task_id'])
        log = m3Area(text=self.task.get_state().get('log'), height=560)
        log.display_text_color = 'white'
        log.appearance = 'outlined'
        log.background_color = 'black'
        alert(log, large=True)

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
        with server.no_loading_indicator:
            self.task_check_timer.interval = 0
            if self.task is None:
                self.task = server.call('getTaskById', self.plano_dropdown_menu.selected_value.tarefa['task_id'])
            
            state = self.task.get_state()
            progress = state.get('progress')
            step = state.get('step')
            message = state.get('message')
            status = state.get('status')
    
            if progress:
                self.geracao_progress_indicator.type = 'determinate'
                self.geracao_progress_indicator.progress = progress
                self.geracao_progress_indicator.tooltip = f"{progress}%"
                self.percentage_text.text = f"{round(progress, 2)}%"
            self.tarefa_status_text.visible = step or message
            self.tarefa_status_text.content = f"**Passo {step}:** {message}"
            if status == 'COMPLETED':
                self.geracao_progress_indicator.progress = 100
                self.percentage_text.text = "100%"
                self.vo = server.call(
                    'getPlanoAlimentarReport', self.plano_dropdown_menu.selected_value['Sequence'], 
                    False, False
                )
                self.ver_receita_button.visible = True
            if status == 'ABORTED':
                self.geracao_progress_indicator.progress_color = 'var(--anvil-m3-error)'
                self.show_log_button.visible = True
            self.task_check_timer.interval = 1

    def number_box_change(self, **event_args):
        """This method is called when the text in this component is edited."""
        number_box = event_args['sender']
        if isinstance(number_box.text, float):
            number_box.text = max(number_box.text, 1)

    
