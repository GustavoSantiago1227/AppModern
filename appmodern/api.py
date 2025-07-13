import webview
import threading
import json

class Api:
    def __init__(self):
        self.data = {}
        self.routes = {}

        # Novo: Evento para sinalizar a chegada de dados do JS
        self._read_event = threading.Event()
        # Novo: Variável para armazenar o resultado da leitura do JS
        self._read_result = None

    def insert_components(self, *components):
        """
                Converte instâncias de componentes em estruturas de dados prontas para o frontend.

                Parâmetros:
                    *components: Um ou mais objetos derivados da classe Tag.
                """
        data = [component.get_data() for component in components]
        self.data = {'data': data}

    def get_data(self):
        data = self.data
        self.data = None
        return data

    def get_window(self):
        return webview.windows[0]

    def create(self, *args):
        self.insert_components(*args)
        window = self.get_window()
        window.evaluate_js('create()')

    def delete(self, *args):
        self.insert_components(*args)
        window = self.get_window()
        window.evaluate_js('del()')

    def read(self, *args):
        self.insert_components(*args) # Prepara os componentes para o JS filtrar/ler
        window = self.get_window()

        self._read_event.clear() # Limpa o evento antes de fazer a chamada
        window.evaluate_js("read()") # Dispara a leitura no JS

        # Espera até que o JS chame read_callback
        self._read_event.wait(timeout=60) # Adiciona um timeout para evitar bloqueio infinito
        if not self._read_event.is_set():
            # Se o timeout expirar e o evento não for disparado
            print("Erro: Timeout ao esperar dados do JavaScript na função read().")
            return None # Retorna None ou lança uma exceção

        result = self._read_result # Pega o resultado
        self._read_result = None # Limpa o resultado para a próxima chamada
        return result

    # Nova função: Recebe o resultado da leitura do JavaScript
    def read_callback(self, data):
        self._read_result = data  # Armazena os dados
        self._read_event.set()  # Sinaliza que os dados chegaram


    def insert_components_in_tuple(self, *components):
        data = []
        for components_to_update in components:
            before, after = components_to_update
            data.append(
                {'before': before.get_data(),
                 'after': after.get_data(),
                 },
            )
        self.data = {'data': data}


    def update(self,*args):
        self.insert_components_in_tuple(*args)
        window = self.get_window()
        window.evaluate_js('update()')





    def route_exec(self, name):
        """Executa a função associada a uma rota registrada."""
        func = self.routes.get(name)
        if not func:
            raise ValueError(f"Rota '{name}' não registrada.")
        func()

    def console(self, msg):
        print(msg)

    def loading(self):
        window = self.get_window()
        window.evaluate_js('loading_head()')
        try:
            self.route_exec('')
        except:
            try:
                self.route_exec('home')
            except:
                raise ValueError(f'Route not definidation')





