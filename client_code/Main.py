from . import Routes
from OruData.Environment import Environment
from .Commons import LocalCommons, call_async

def load_funcionalidades():
    """Realiza um import inicial para que ocorra o registro das versões"""
    from . import Changelog
    return

def override_entities():
    from OruData import Entity
    from . import Entities
    Entity.User = Entities.ProfissionalUser

def main():
    call_async(load_funcionalidades)
    override_entities()
    with Environment().startup(use_fcm=False):
        call_async(LocalCommons().start)
        Routes.launch()

if __name__ == "__main__":
    main()