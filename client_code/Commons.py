from OruData.Globals import CommonData, singleton_class, call_async

def after_login_method(user, context=None, **event_args):
    from OruData.Routing import navigate
    if user is not None and not (user['fullname'] and user['display_name'] and user['cpf']):
        navigate(path='/user/init')
        return True
    elif user is not None:
        navigate(path='/dashboard')
        return True

@singleton_class(merge_subclass=True)
class LocalCommons(CommonData):
    _profissional = None
    _profissional_async_call = None

    _pacientes = None
    _pacientes_async_call = None

    def start(self, ambiente=None):
        CommonData.start(self)
        self.ambiente = ambiente
    
    def load_data(self):
        CommonData.load_data(self)
        self._refresh_profissional()
        self._refresh_pacientes()

    def clear_data(self):
        CommonData.clear_data(self)
        self._profissional = None
        self._profissional_async_call = None
        self._pacientes = None
        self._pacientes_async_call = None

    # INIT METHODS
    def _set_pacientes(self, pacientes):
        from .Entities import Paciente
        self._pacientes = Paciente.from_search(pacientes)

    def _set_profissional(self, profissional):
        from .Entities import Profissional
        self._profissional = Profissional(profissional)

    def _refresh_pacientes(self):
        self._pacientes_async_call = call_async('getPacienteByUser')
        self._pacientes_async_call.on_result(self._set_pacientes)

    def _refresh_profissional(self):
        self._profissional_async_call = call_async('getProfissionalByUser', user=self._logged_user)
        self._profissional_async_call.on_result(self._set_profissional)

    # VERIFY METHOS
    def _wait_for_pacientes(self):
        if self._pacientes_async_call is None:
            if self.get_logged_user() is None:
                return
            self._refresh_pacientes()
        if self._pacientes_async_call.status == "PENDING":
            from anvil import server
            with server.loading_indicator():
                self._set_pacientes(self._pacientes_async_call.await_result())

    def _wait_for_profissional(self):
        if self._profissional_async_call is None:
            if self.get_logged_user() is None:
                return
            self._refresh_profissional()
        if self._profissional_async_call.status == "PENDING":
            self._set_profissional(self._profissional_async_call.await_result())

    # GET METHODS
    @property
    def profissional(self):
        self._wait_for_profissional()
        return self._profissional

    def get_pacientes(self):
        self._wait_for_pacientes()
        return self._pacientes