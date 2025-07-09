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

## Exemplo de Uso

Aqui está um exemplo simples de uma aplicação de login, como visto na pasta `exemples/`.

**`main.py`**
```python
from appmodern.app import App
from appmodern.components import StyleExternal
import exemples.home # Importa as rotas da aplicação

app = App(title="Login", debug=True, lang='pt-br')
app.head.add_childrens(
    StyleExternal('style.css')
)
app.run()
```

**`home.py`** (onde a lógica da UI e as rotas são definidas)
```python
from appmodern.components import Tag
from appmodern import route, create, read

class Div(Tag):
    # ... (custom components)

@route('home')
def home_page():
    create(
        Div('body',
            # ... (criação da UI)
            id='div-login',
        )
    )

@route('logar')
def logar():
    data = read(Input(id='login'), Input(id='password'))
    # ... (lógica de login)
```

## Como Funciona

A biblioteca funciona da seguinte forma:
1.  A classe `App` inicializa uma janela `pywebview`.
2.  Componentes baseados na classe `Tag` são usados para definir a estrutura HTML em Python.
3.  As funções `create`, `read`, `update` e `delete` manipulam o DOM da página web em tempo real, comunicando-se com o JavaScript através da `Api` interna.
4.  O decorador `@route` permite que funções Python sejam chamadas diretamente a partir de eventos no JavaScript (como cliques de botão).

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.