class Tag:
    def __init__(self, parent='body', *children, **attrs):
        """
        Classe base para representação de uma tag HTML genérica, com suporte à composição hierárquica.

        Esta classe fornece a estrutura necessária para modelar elementos HTML, incluindo o nome da tag,
        atributos e filhos, permitindo a construção de uma árvore DOM representada em Python.

        Parâmetros:
            parent (str): Nome da tag pai, usado para referência estrutural. Padrão: 'body'.
            *childrens: Elementos filhos, podendo ser objetos Tag ou strings (conteúdo textual).
            **attrs: Atributos HTML, onde nomes Python-friendly (ex: class_) são convertidos adequadamente.

        Atributos:
            element (str): Nome da tag inferido pelo nome da subclasse (ex: 'div', 'span').
            attributes (dict): Dicionário de atributos convertidos para nomenclatura HTML válida.
            childrens (list): Lista de elementos filhos.
        """
        self.parent = parent
        self.element = self.__class__.__name__.lower()

        if self.element == 'tag':
            raise NotImplementedError(
                "A classe base 'Tag' não deve ser instanciada diretamente. "
                "Utilize uma subclasse específica como 'Div', 'Span', etc."
            )

        self.attributes = {}
        self.update_attributes(**attrs)
        self.children = []
        self.add_children(*children)

    def add_children(self, *children):
        """Adiciona elementos filhos à tag atual."""
        self.children += list(children)

    def update_attributes(self, **attrs):
        """
        Atualiza os atributos HTML da tag com base em convenções Python-friendly.

        Exemplo: 'class_' é convertido para 'class', e 'data_id' vira 'data-id'.
        """
        for key, value in attrs.items():
            if key == 'class_':
                self.attributes['class'] = value
            else:
                self.attributes[key.replace('_', '-')] = value

    def get_data(self):
        """
        Retorna uma estrutura de dados aninhada que representa a tag e seus descendentes.

        Útil para serialização (ex: para consumo em Javascript).
        """
        data = {
            'parent': self.parent,
            'element': self.element,
            'attributes': self.attributes,
            'children': []
        }

        for children in self.children:
            if isinstance(children, Tag):
                data['children'].append(children.get_data())
            else:
                data['children'].append(children)

        return data

    def info(self, *args):
        """
        Exibe informações detalhadas sobre a tag no console, com a possibilidade de filtragem.

        Parâmetros:
            *args: Lista de chaves específicas a serem exibidas (opcional).
        """
        full_data = self.get_data()
        data = {key: full_data[key] for key in args} if args else full_data

        print("INFORMAÇÕES DA TAG:", self.element)
        for key, value in data.items():
            print(f'Chave: {key}')
            if key == 'attributes':
                for attr, val in value.items():
                    print(f'  Atributo: {attr} -> {val}')
            elif key == 'children':
                for child in value:
                    if isinstance(child, dict):
                        print(f"  Filho: {child.get('element', 'texto')}")
                    else:
                        print(f"  Conteúdo: {child}")
            else:
                print(f'  Valor: {value}')



class ScriptExternal(Tag):
    """Representa um <script> com fonte externa (arquivo JavaScript separado)."""
    def __init__(self, parent=None, src=''):
        super().__init__(parent, type='text/javascript', src=src)
        self.element = 'script'




class StyleExternal(Tag):
    """Representa um link para um arquivo CSS externo, utilizando a tag <link> apropriada."""
    def __init__(self, href=''):
        super().__init__('head', rel='stylesheet', href=href)
        self.element = 'link'


class Meta(Tag):
    def __init__(self, parent='head', *children, **attrs):
        super().__init__(parent, *children, **attrs)


class Title(Tag):
    def __init__(self, parent='head', *children, **attrs):
        super().__init__(parent, *children, **attrs)





class Head(Tag):
    """
    Representa a seção <head> do documento HTML.

    Inicializa com metadados padrão, incluindo charset, viewport e título da página.
    Permite inclusão de elementos adicionais como scripts, links e estilos.
    """
    def __init__(self, title=None):
        super().__init__('html',
    Meta('head', charset='UTF-8'),
            Meta('head',  name='viewport', content="width=device-width, initial-scale=1.0"),
            Title('head', title))




class Body(Tag):
    """
    Representa a seção <body> do documento HTML, contendo todo o conteúdo visível da página.
    """
    def __init__(self, *children, **attrs):
        super().__init__('html', *children, **attrs)
        self.element = 'body'




class Item:
    def __init__(self, value):
        self.id = value.get('id')
        self.class_ = value.get('class')
        self.name = value.get('name')
        self.element = value.get('element')
        self.value = value.get('value')
        self.text = value.get('text')
        self.html = value.get('html')



class Data:
    def __init__(self, data):
        self.data = [Item(value) for value in data['data']]

    def get(self):
        return self.data





