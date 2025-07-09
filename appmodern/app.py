import webview  # Biblioteca que fornece integração com janelas HTML/JS nativas
from appmodern import api
from appmodern.components import Head
from appmodern.create_page import page
class App:
    """
    Classe principal responsável por configurar e iniciar a aplicação visual em uma janela WebView.

    Permite personalização do título, idioma, layout da interface, dimensões da janela
    e execução em modo debug ou tela cheia.
    """
    def __init__(self, title="My program",
                 width=800, height=600, full_screen=False,
                 debug=False, lang='en'):
        self.title = title
        self.width = width
        self.height = height
        self.full_screen = full_screen
        self.lang = lang
        self.head = Head(self.title)  # Gera o cabeçalho com metadados e título
        self.debug = debug
        self.window = None

    def create_components_head(self):
        """
        Cria os componentes HTML principais da página, como título e layout do corpo.
        Substitui pelo conteúdo customizado, se fornecido.
        """
        #api.insert_components_in_api(self.header)
        api.insert_components(self.head)

    def template_html(self):
        """
        Gera o HTML e salva no diretório especificado.
        """
        page(self.lang)

    def create_window(self):
        """
        Cria e configura a janela WebView com os parâmetros definidos na instância.
        """
        webview.create_window(
            title=self.title,
            url=f'static/index.html',
            js_api=api,
            width=self.width,
            height=self.height,
            fullscreen=self.full_screen
        )

    def run(self):
        """
        Executa o ciclo completo da aplicação:
            - Criação dos componentes
            - Geração do HTML
            - Inicialização da janela WebView
        """
        self.create_components_head()
        self.template_html()
        self.create_window()
        webview.start(debug=self.debug)