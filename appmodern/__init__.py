from .api import Api
from .components import Data
api = Api()


def route(name):
    """Decorador para registrar funções como rotas nomeadas."""
    def decorator(func):
        if not hasattr(api, 'routes'):
            api.routes = {}
        api.routes[name] = func
        return func
    return decorator


def create(*args):
    api.create(*args)

def delete(*args):
    api.delete(*args)


# A função read de nível superior (appmodern)
def read(*args):
    # Chama o método read da sua instância de API, que agora espera pelo resultado do JS
    return Data(api.read(*args)) # Assumindo que 'api' é a instância da sua classe Api


def update(*args):
    api.update(*args)

