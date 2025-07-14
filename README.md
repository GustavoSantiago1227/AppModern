# AppModern

[![PyPI version](https://badge.fury.io/py/appmodern.svg)](https://badge.fury.io/py/appmodern)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`AppModern` é uma biblioteca Python para criar facilmente aplicações de desktop com interfaces web (HTML, CSS, JS), utilizando o poder do `pywebview`.

## Visão Geral

A biblioteca abstrai a complexidade da comunicação entre Python e JavaScript, permitindo que você construa a interface do usuário com componentes Python que são renderizados dinamicamente no frontend.

## Instalação

Você pode instalar o `AppModern` via pip:

```bash
pip install appmodern
```

#### Como Usar
Toda aplicação possui duas classes principais: App e api.

`App` Responsável por gerar a interface principal com a janela web.

`Api` Responsável pela comunicação entre o frontend e o backend Python..


#### App

O `App`  é o núcleo da aplicação. Ele carrega a janela HTML do PyWebView e gerencia o conteúdo.


```python
from appmodern.app import App

app = App(
    title="My Program",
    width=800,
    height=600,
    full_screen=False,
    debug=False,
    lang='en'
)

# Adiciona filhos extras à tag <head>
app.head.add_children(
    # Componentes como folhas de estilo ou scripts externos
)

# Inicializa a aplicação
app.run()

```


#### Componentes
A manipulação do DOM é feita através de componentes Python. Os principais são:

`Tag` (classe genérica para criação de elementos HTML)

`ScriptExternal, StyleExternal, Meta, Title, Head, Body`

```python
from appmodern.components import Tag

# Classe personalizada baseada em uma <div>
class Div(Tag):
    pass

# Estrutura com filhos e atributos
class DivBlock(Tag):
    def __init__(self, parent, *children, **kwargs):
        """
        parent: seletor CSS para o elemento pai (ex: 'body', '#id', '.class')
        children: outros componentes (tags) filhos
        kwargs: atributos HTML (id, class_, style, value, etc.)
        """
        super().__init__(parent, *children, class_="exemplo", **kwargs)
        self.element = 'div'  # Corrige o nome da tag HTML


```
**Observação:** Por padrão, o nome da tag `HTML` será o nome da classe. Se necessário, sobrescreva self.element para garantir compatibilidade com o **HTML**




#### 🧠 API

A `Api` é a classe responsável pela comunicação entre o backend (Python) e o frontend (JavaScript).  
Ela atua com **seis funções principais no Python** e **cinco no JavaScript**, sendo elas:

- `route`
- `call`
- `create`
- `read`
- `update`
- `delete`

---

```python
from appmodern import route, call, create, read, update, delete
from appmodern.components import Tag

# Criando componentes personalizados
class P(Tag): pass
class Button(Tag): pass

# Decorador para registrar uma rota que será chamada pelo frontend
# A função 'home' será executada automaticamente ao iniciar a aplicação
@route('home')
def sua_funcao(*args, **kwargs):
    # Cria um parágrafo na tag <body>
    create(P("body", "Texto"))

    # Lê elementos com base em seletores CSS
    # Filtros disponíveis: 'text', 'html', 'value', 'style'
    read('p', filter=['text', 'html', 'value', 'style'])

    # Atualiza o conteúdo de elementos com base em um seletor
    update(('p', P('body', "Atualiza aqui")))

    # Remove elementos do DOM com base em seletores
    delete('p')

    # Cria um botão com ação de clique que chama uma função Python
    create(Button('body', "Clique", onclick="call('clique')"))

# Rota que será chamada ao clicar no botão
@route('clique')
def uso_do_call(*args, **kwargs):
    # call() é uma função de comunicação entre front e back.
    # Pode ser usada em ambos os lados para invocar funções.
    # Parâmetros:
    #   call(nome_da_função, lista_de_args, dicionario_de_kwargs)

    call('funcao_de_apresentacao', ['arg1', 'arg2'], {"kwarg": 1})
```


### Exemplo pratico

`main.py`
```python
from appmodern.app import App
import exemples.home
app = App(
    title="AppModern Login",
    width=800,
    height=600,
    full_screen=False,
    debug=True,
    lang='pt-BR'
)

# Roda a aplicação
app.run()
```
`home.py`

```python
#Componentes
from appmodern.components import Tag

class Div(Tag): pass
class Button(Tag): pass
class Input(Tag): pass
class Label(Tag): pass
class H1(Tag): pass
class P(Tag): pass


#Tela de login
from appmodern.components import Tag
from appmodern import route, create, read, update, delete, call
from time import sleep

# Componentes personalizados
class Div(Tag):
    def __init__(self, parent='body', *children, **kwargs):
        style = kwargs.pop("style", "") + """
            display: flex;
            flex-direction: column;
            align-items: center;
            background: #ffffff;
            padding: 30px;
            margin: 10% auto;
            width: 300px;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            font-family: 'Segoe UI', sans-serif;
        """
        super().__init__(parent, *children, style=style, **kwargs)

class Label(Tag):
    def __init__(self, parent='body', *children, **kwargs):
        style = kwargs.pop("style", "") + "margin-top: 12px; width: 100%; color: #444; font-weight: bold;"
        super().__init__(parent, *children, style=style, **kwargs)

class Input(Tag):
    def __init__(self, parent='body', **kwargs):
        style = kwargs.pop("style", "") + """
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-top: 6px;
        """
        super().__init__(parent, style=style, **kwargs)

class Button(Tag):
    def __init__(self, parent='body', *children, **kwargs):
        style = kwargs.pop("style", "") + """
            background-color: #4facfe;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 20px;
            width: 100%;
        """
        super().__init__(parent, *children, style=style, **kwargs)

class H1(Tag): pass
class H2(Tag): pass
class P(Tag): pass

# Página inicial com formulário de login
@route('home')
def home_page():
    create(
        Div('body',
            H1(None, 'Login'),
            Label(None, "Login", Input(None, type="text", id='login')),
            Label(None, "Senha", Input(None, type="password", id='password')),
            Button(None, "Logar", onclick='call("logar")'),
            id='div-login'
        )
    )

# Função chamada ao clicar em "Logar"
@route('logar')
def logar():
    data = read('input', filter=['value'])
    login, password = data['data']

    if login[0] == 'gustavo' and password[0] == '123':
        call('bem-vindo', [login[0], 5])
    else:
        data = read('p')
        if not data['data']:
            create(P('#div-login', 'Login ou senha incorretos'))

# Simula tela de carregamento com contagem regressiva
@route('bem-vindo')
def bem_vindo(nome, segs):
    if segs == 5:
        delete('#div-login')
        create(
            Div('body',
                H1(None, 'Seja Bem-vindo'),
                P(None, f'{nome}, o programa ficará pronto em {segs}s'),
                id="div-bem-vindo"
            )
        )
        bem_vindo(nome, segs - 1)
    elif segs > 0:
        sleep(1)
        update(('p', P(None, f'{nome}, o programa ficará pronto em {segs}s')))
        bem_vindo(nome, segs - 1)
    else:
        update(('div#div-bem-vindo',
            Div(None,
                H1(None, "Logado com sucesso"),
                P(None, f"{nome}, seja muito bem-vindo ao novo sistema"),
                id="div-bem-vindo")
        ))
        create(H2('#div-bem-vindo', "AppModern"))

```


## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.