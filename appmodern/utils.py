
import os

def create_folder():
    """
    Cria a pasta static caso ela não exista para garantir que a aplicação ocorrerar conforme o esperado
    :return:
    """
    name = 'static'
    if not os.path.exists(name):
        os.makedirs(name)

def loading_file(path):
    """
    Lê o conteúdo de um arquivo a partir do caminho especificado.

    Parâmetros:
        path (str): Caminho completo para o arquivo a ser lido.

    Retorna:
        str: Conteúdo do arquivo em formato de string.
    """
    with open(path, 'r') as f:
        file = f.read()
    return file


def create_file(path, data):
    """
    Cria ou sobrescreve um arquivo no caminho especificado com os dados fornecidos.

    Parâmetros:
        path (str): Caminho onde o arquivo será criado.
        data (str): Conteúdo que será escrito no arquivo.
    """
    with open(path, 'w') as f:
        f.write(data)



