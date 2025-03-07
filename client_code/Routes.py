from anvil import app

from OruData.Routing import launch, Route, CrudRoute, Redirect, SecureRoute as BaseSecureRoute
# from .Entities import 

IN_DEBUG_MODE = "debug" in app.environment.tags

# if not IN_DEBUG_MODE:
    # Route.error_form = "Pages.Utils.ErrorForm"

def is_user_logged():
    from .Commons import LocalCommons
    logged_user = LocalCommons().get_logged_user_forced()
    return logged_user

class UnloggedRoute:
    if not IN_DEBUG_MODE:
        error_form = "Pages.Utils.ErrorFormUnlogged"
    
    def before_load(self, **loader_args):
        from .Commons import LocalCommons
        if LocalCommons().get_logged_user_forced():
            raise Redirect(path="/dashboard")

class SecureRoute(BaseSecureRoute):
    """Todas as rotas seguras devem antes checar se o usuário logado já completou o cadastro também.
    Se não está logado, redireciona ao login.
    Se está logado e não completou o cadastro, redireciona ao init
    """
    if not IN_DEBUG_MODE:
        error_form = "Pages.Utils.ErrorForm"
    
    def before_load(self, **loader_args):
        user = BaseSecureRoute.before_load(self, **loader_args)
        # Se chegou aqui, então está logado
        if not (user['fullname'] and user['display_name'] and user['cpf']):
            raise Redirect('/user/init')

# Main
class HomeRoute(UnloggedRoute, Route):
    path = '/'
    form = 'Pages.Home'
    
class DashboardRoute(SecureRoute, Route):
    path = '/dashboard'
    form = 'Pages.Dashboard'

# Outros
class AboutRoute(Route):
    path = '/about'
    
    @property
    def form(self):
        if is_user_logged():
            return "Pages.Outros.About"
        return 'Pages.Outros.AboutUnlogged'
    
class ChangelogRoute(SecureRoute, Route):
    path = '/changelog'
    form = "Pages.Outros.Changelog"

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
    cache_form = False
    default_not_found = True

    @property
    def form(self):
        if is_user_logged():
            return "Pages.Utils.NotFound"
        return "Pages.Utils.NotFoundUnlogged"