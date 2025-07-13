from appmodern.app import App
from appmodern.components import StyleExternal, ScriptExternal
import exemples.home
app = App(title="Login", debug=True, lang='pt-br')
app.head.add_childrens(
    StyleExternal('style.css')
)
app.run()