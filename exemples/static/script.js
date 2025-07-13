
/**
 * L� elementos do DOM com base nos dados recebidos do backend,
 * filtra e envia o resultado de volta para o Python.
 */
async function read() {
    // Solicita ao backend os crit�rios de busca para os elementos
    const data = await window.pywebview.api.get_data();
    let values = selectElement(data.data.args, data.data.filter);
    // Envia os dados extra�dos de volta ao Python para manipula��o posterior
    window.pywebview.api.read_callback({ data: values});
}



function filterValuesFromElement(element, filter) {
    let values = [];
     const map = {
        value: element => element.value ?? null,
        text: element => element.innerText,
        html: elementel => element.innerHTML,
        style: element => element.getAttribute('style') ?? ''
    };

    return filter.map(key => map[key]?.(element) ?? null);
}



function selectElement(args, filter) {
    var data = [];
    args.forEach(arg => {
        let query = document.querySelectorAll(arg);
        if (query && query.length > 0) {
            query.forEach(elements => {
            data.push(filterValuesFromElement(elements, filter));
            });
        }
        else{
            msg('Nenhum elemento foi selecionado em:', arg);
        }
    });

    console.log(data);
    return data;
}


/**
 * Cria e insere dinamicamente elementos HTML com base nos dados recebidos do Python.
 * Os elementos sao registrados na estrutura de componentes local.
 */
async function create() {
    try {
        let data = await window.pywebview.api.get_data();
        if (data) {
        render(data.data);
        }
    } catch (error) {
        msg('Erro ao carregar elemento no DOM:', error);
    }
    
}


/**
 * Executa uma rota registrada via PyWebView, disparando a função Python correspondente.
 *
 * @param {string} function_route - Nome da rota a ser acionada no backend.
 * @param {Array} args_list - Lista de argumentos posicionais a serem passados para a função.
 * @param {Object} kwargs - Objeto contendo os argumentos nomeados (keyword arguments).
 */
function call(function_route, args_list = [], kwargs = {}) {
    window.pywebview.api.route_exec(function_route, args_list, kwargs);
}




/**
 * Cria dinamicamente os elementos da seção <head> da página,
 * utilizando os dados iniciais enviados pelo backend Python via PyWebView.
 */
async function loading_head() {
    try {
        const data = await window.pywebview.api.get_data();
        if (data) {
            render(data.data[0].children);
        } else {
            msg('Não existem elementos para adicionar no <head>!');
        }
    } catch (error) {
        msg('Erro ao carregar elementos do <head>:', error);
    }
}



/**
 * Renderiza dinamicamente elementos no <head> da página,
 * com base nos dados recebidos do backend.
 * 
 * @param {Array} data - Lista de objetos contendo os dados dos elementos a serem criados.
 */
function render(data) {
    data.forEach(element => {
        new CreateElement(
            element.parent,
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
            if (typeof element === 'string' || typeof element === 'number') {
                this.element.innerText += element;
            }
            else{
                new CreateElement(
                this.element,
                element.element,
                element.attributes,
                element.children
            );
            }
            
        } catch (error) {
            msg('Erro ao criar filho de ' + this.element, error);
            
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
function msg(msg, error) {
    window.pywebview.api.console(msg);
    window.pywebview.api.console(`${error}`);
}



/**
 * Evento disparado quando o PyWebView termina de carregar.
 * Inicia o carregamento da seção <head> da página utilizando a API do backend em Python.
 */
window.addEventListener('pywebviewready', function () {
    try {
        window.pywebview.api.loading();
    } catch (error) {
        msg('Falha na comunicação com o backend!', error);
    }
});
