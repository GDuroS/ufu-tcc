import anvil.server
from OruData.Entity import Entity, User, EntityDescriptor

class ProfissionalUser(User):
    
    @classmethod
    def load_user(cls, buffer_changes=False):
        obj = super(buffer_changes)
        obj.profissional = Profissional.load_by_user(obj)
        return obj

class Profissional(Entity):
    user = EntityDescriptor(ProfissionalUser)

    @classmethod
    def load_by_user(cls, user):
        if isinstance(user, ProfissionalUser):
            user_obj = user
            user = user_obj.original_row
        else:
            user_obj = None
        obj = cls(anvil.server.call('getProfissionalByUser', user=user))
        if obj.is_new:
            obj['user'] = user
        if user_obj:
            obj._user_class = user_obj
        return obj