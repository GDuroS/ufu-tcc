from OruData.Globals import CommonData, singleton_class, call_async

def after_login_method(user, context=None, **event_args):
    if user is not None and not (user['fullname'] and user['display_name'] and user['cpf']):
        from OruData.Routing import navigate
        navigate(path='/user/init')
        return True

@singleton_class(merge_subclass=True)
class LocalCommons(CommonData):
    pass
    # def load_data(self):
    #     CommonData.load_data(self)
    #     after_login_method(self._logged_user)