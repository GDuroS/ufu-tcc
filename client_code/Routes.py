from anvil import app

from OruData.Routing import launch, Route, CrudRoute, UnloggedRoute, Redirect, SecureRoute as BaseSecureRoute
# from .Entities import 

IN_DEBUG_MODE = "debug" in app.environment.tags

if not IN_DEBUG_MODE:
    Route.error_form = "Pages.Utils.ErrorForm"
# Main
Route.create(path='/', form='Pages.Dashboard')

# Outros
Route.create(path="/about", form="Pages.Outros.About")
Route.create(path='/changelog', form="Pages.Outros.Changelog")

class SecureRoute(BaseSecureRoute):
    """Todas as rotas seguras devem antes checar se o usuário logado já completou o cadastro também.
    Se não está logado, redireciona ao login.
    Se está logado e não completou o cadastro, redireciona ao init
    """
    def before_load(self, **loader_args):
        user = BaseSecureRoute.before_load(self, **loader_args)
        # Se chegou aqui, então está logado
        if not (user['fullname'] and user['display_name'] and user['cpf']):
            raise Redirect('/user/init')

# Users
class UserSetup(BaseSecureRoute, Route):
    # Precisa ser BaseSecureRoute para não causar recursão
    path = "/user/init"
    form = "Components.Users.IdentidadesForm"

class UserIdentity(SecureRoute, Route):
    path = "/user/config"
    form = "Pages.Users.Identidades"

# Aux
class LoginForm(UnloggedRoute, Route):
    form = "Pages.Utils.LoginForm"

class LoginRoute(LoginForm):
    path = "/login"

class SignupRoute(LoginForm):
    path = "/signup"

class NotFoundRoute(Route):
    form = "Pages.Utils.NotFound"
    cache_form = False
    default_not_found = True