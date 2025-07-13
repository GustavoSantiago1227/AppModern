
/**
 * Cria dinamicamente os elementos da seção <head> da página,
 * utilizando os dados iniciais enviados pelo backend Python via PyWebView.
 */
async function loading_head() {
    try {
        const data = await window.pywebview.api.get_data();
        
        if (data && data.data && data.data[0] && data.data[0].children) {
            render(data.data[0].children);
            msg('Cabeçalho carregado com sucesso!');
        } else {
            msg('Não existem elementos para adicionar no <head>!');
        }
        
    } catch (error) {
        msg('Erro ao carregar elementos do <head>:');
        msg(error);
    }
}



/**
 * Renderiza dinamicamente elementos no <head> da página,
 * com base nos dados recebidos do backend.
 * 
 * @param {Array} data - Lista de objetos contendo os dados dos elementos a serem criados.
 */
function render(data) {
    console.log(data);
    data.forEach(element => {
        new CreateElement(
            document.head,
            element.element,
            element.attributes,
            element.children
        );
    });
}




/**
 * Classe responsável pela criação dinâmica de elementos HTML, 
 * com atributos, filhos e inserção opcional no DOM.
 */
class CreateElement {
    /**
     * Construtor da classe CreateElement.
     * 
     * @param {HTMLElement|string} parent - Elemento pai ou seletor CSS onde o novo elemento será inserido.
     * @param {string} element - Tipo da tag HTML a ser criada (ex: 'div', 'span').
     * @param {Object} attributes - Objeto contendo os atributos HTML do elemento.
     * @param {Array} children - Lista de filhos (elementos ou textos) a serem inseridos.
     * @param {boolean} insert - Define se o novo elemento será automaticamente inserido no DOM (padrão: true).
     */
    constructor(parent, element, attributes, children, insert = true) {
        this.parent = (typeof parent === 'string') ? document.querySelector(parent) : parent;
        this.element = document.createElement(element);
        this.setAttributes(attributes);
        this.forEachChildren(children);
        if (insert) {
            this.insertElement();
        }
    }

    /**
     * Insere o elemento criado como filho do elemento pai no DOM.
     */
    insertElement() {
        this.parent.appendChild(this.element);
    }

    /**
     * Cria e adiciona um filho ao elemento principal.
     * Aceita um objeto com especificação de elemento dinâmico
     * ou um valor simples (string/número) como texto.
     * 
     * @param {Object|string|number} element - Elemento filho ou conteúdo textual.
     */
    createChildren(element) {
        try {
            new CreateElement(
                this.element,
                element.element,
                element.attributes,
                element.children
            );
        } catch (error) {
            if (typeof element === 'string' || typeof element === 'number') {
                this.element.innerText += element;
            }
        }
    }

    /**
     * Itera sobre os filhos declarados e os adiciona ao elemento.
     * 
     * @param {Array} children - Lista de filhos a serem processados.
     */
    forEachChildren(children) {
        if (!Array.isArray(children)) return;
        children.forEach(child => this.createChildren(child));
    }

    /**
     * Define os atributos HTML fornecidos no elemento.
     * 
     * @param {Object} attributes - Objeto contendo os atributos no formato chave/valor.
     */
    setAttributes(attributes) {
        if (attributes && typeof attributes === 'object') {
            for (const [key, value] of Object.entries(attributes)) {
                this.element.setAttribute(key, value);
            }
        }
    }
}





/**
 * Envia mensagens do JavaScript para o console do backend Python via PyWebView.
 *
 * @param {string} msg - Mensagem a ser enviada ao console Python.
 */
function msg(msg) {
    window.pywebview.api.console(msg);
}



/**
 * Evento disparado quando o PyWebView termina de carregar.
 * Inicia o carregamento da seção <head> da página utilizando a API do backend em Python.
 */
window.addEventListener('pywebviewready', function () {
    try {
        msg('Comunicação bem-sucedida!');
        window.pywebview.api.loading();
    } catch (error) {
        msg('Falha na comunicação com o backend!');
        msg(error);
    }
});
