# scripts
import anvil.server

@anvil.server.callable
def postSomethingAndLog(something, attribute_to_show=None):
    print(something)
    if attribute_to_show:
        print(getattr(something, attribute_to_show))