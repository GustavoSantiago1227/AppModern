from appmodern.utils import create_file, create_folder


def page(lang):
    """
    Gera uma estrutura básica de página HTML e salva em disco no caminho especificado.

    Parâmetros:
        path (str): Caminho do arquivo HTML que será criado (ex: 'index.html').
        lang (str): Código de idioma para o atributo 'lang' da tag <html> (ex: 'pt-br', 'en').
        title (str): Título da página a ser inserido na tag <title>.

    A estrutura gerada inclui:
        - Declaração do DOCTYPE HTML5
        - Abertura da tag <html> com atributo 'lang'
        - Tags <head> e <body> básicas
        - Inclusão de um <script> externo com id 'main-reserve'
    """
    html = f"""
<!DOCTYPE html>
<html lang="{lang}">
<head>
   
    <script class="main-reserve" src="script.js"></script>
</head>
<body>
</body>
</html>"""
    create_folder()
    create_file(f'static/index.html', html)  # Grava o conteúdo no caminho especificado