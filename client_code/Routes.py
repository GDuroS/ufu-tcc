from anvil import app

from OruData.Routing import launch, Route, SecureRoute, CrudRoute, UnloggedRoute, Redirect
# from .Entities import 

IN_DEBUG_MODE = "debug" in app.environment.tags

if not IN_DEBUG_MODE:
    Route.error_form = "Pages.Utils.ErrorForm"
# Main
Route.create(path='/', form='Pages.Dashboard')

# Outros
Route.create(path="/about", form="Pages.Outros.About")
Route.create(path='/changelog', form="Pages.Outros.Changelog")

# Users
class UserSetup(SecureRoute, Route):
    path = "/user/setup"
    form = "Components.Users.IdentidadesForm"

class UserIdentity(SecureRoute, Route):
    path = "/user/config"
    form = "Pages.Users.Identidades"

# Aux
class LoginForm(UnloggedRoute, Route):
    form = "Pages.Utils.LoginForm"

class LoginRoute(LoginForm):
    path = "/login"

class SignupRoute:
    path = "/signup"

class NotFoundRoute(Route):
    form = "Pages.Utils.NotFound"
    cache_form = False
    default_not_found = True