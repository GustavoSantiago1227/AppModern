from appmodern.components import Tag
from appmodern import route, create, read, update

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

class H1(Tag):
    def __init__(self, parent='body', *children, **kwargs):
        style = kwargs.pop("style", "") + "margin-bottom: 24px; color: #333;"
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




class P(Tag):
    pass


@route('logar')
def logar():

    data = read(Input(id='login'), Input(id='password'))
    values = tuple(item.value for item in data.get())
    log = ''
    if values != ('gustavo', '123'):
        log = 'Senha ou login incorreto'
    else:
        log = 'Logado'

    paragraph = read(P())
    if len(paragraph.get()) > 0:
        update((P('#div-login'), P('#div-login', log)))
    else:
        create(P('#div-login', log))

    update(
        (Input('#div-login', id="login"), Input('#div-login', id="login", value='')),
        (Input('#div-login', id="password"), Input('#div-login', id="password", value=''))
    )



@route('home')
def home_page():
    create(
        Div('body',
            H1(None, 'Login'),
            Label(None, "Login",
                Input(None, type="text", id='login')),
            Label(None, "Password",
                Input(None, type="password", id='password')),
            Button(None, "Logar", onclick='call("logar")'),
            id='div-login',
        )
    )