from anvil import app

from OruData.Routing import launch, Route, SecureRoute, CrudRoute, UnloggedRoute, Redirect
# from .Entities import 

IN_DEBUG_MODE = "debug" in app.environment.tags

if not IN_DEBUG_MODE:
    Route.error_form = "Pages.Utils.ErrorForm"

