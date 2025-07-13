from appmodern.components import Tag
from appmodern import route, create, read, update, delete, call

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


@route('bem-vindo')
def bem_vindo(nome):
    delete('#div-login')




@route('logar')
def logar():
    data = read( 'input', filter=['value'])
    login, password = data['data']
    if login[0] == 'gustavo' and password[0] == '123':
        call('bem-vindo', [login[0]])
    else:
        data = read('p')
        if not data['data']:
            create(P('#div-login', 'Login ou senha incorretos'))



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