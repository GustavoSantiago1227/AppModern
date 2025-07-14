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
    script = """




/**
 * Classe responsável por atualizar elementos do DOM com base em um novo modelo.
 * Substitui atributos e conteúdo interno dos elementos-alvo.
 */
class UpdateElements {
    /**
     * @param {string} target - Seletor CSS dos elementos a serem atualizados.
     * @param {Object} element - Objeto representando o novo modelo do elemento.
     */
    constructor(target, element) {
        // Seleciona os elementos de origem a serem atualizados
        this.origin_elements = document.querySelectorAll(target);

        // Cria um novo elemento temporário com os dados recebidos, sem inserir no DOM
        const createElement = new CreateElement(
            element.parent,
            element.element,
            element.attributes,
            element.children,
            false
        );

        this.updateElement = createElement.element;

        // Atualiza cada elemento de origem com os dados do novo modelo
        this.origin_elements.forEach(originElement => {
            this.clone(originElement, this.updateElement);
        });
    }

    /**
     * Atualiza um elemento existente com base em outro modelo.
     * 
     * @param {HTMLElement} originElement - Elemento original a ser atualizado.
     * @param {HTMLElement} updateElement - Elemento modelo com os novos dados.
     */
    clone(originElement, updateElement) {
        // Remove todos os atributos antigos
        while (originElement.attributes.length > 0) {
            originElement.removeAttribute(originElement.attributes[0].name);
        }

        // Adiciona os novos atributos do elemento modelo
        for (let attr of updateElement.attributes) {
            originElement.setAttribute(attr.name, attr.value);

            // Atualiza o valor manualmente para inputs e textareas
            if (
                attr.name === 'value' &&
                (originElement.tagName === 'INPUT' || originElement.tagName === 'TEXTAREA')
            ) {
                originElement.value = attr.value;
            }
        }

        // Atualiza o conteúdo interno (HTML)
        originElement.innerHTML = updateElement.innerHTML;
    }
}




/**
 * Atualiza elementos do DOM com base em dados recebidos do backend.
 * Utiliza a classe UpdateElements para aplicar as alterações.
 */
async function update() {
    const data = await window.pywebview.api.get_data();

    if (data && data.data) {
        data.data.forEach(element => {
            new UpdateElements(element.target, element.element);
        });
    }
}




/**
 * Remove elementos do DOM com base nos dados recebidos do backend.
 * Pode ser usada para limpar seções dinâmicas da interface.
 */
async function del() {
    const data = await window.pywebview.api.get_data();

    if (data && data.data) {
        data.data.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => el.remove()); // Remove cada elemento do DOM
        });
    } else {
        msg('Não há conteúdo para deletar em:', data);
    }
}







/**
 * Lê elementos do DOM com base nos dados recebidos do backend,
 * aplica filtros nas propriedades desejadas e envia o resultado de volta para o Python.
 */
async function read() {
    // Solicita ao backend os critérios de busca e filtros de propriedades
    const data = await window.pywebview.api.get_data();

    // Filtra os elementos encontrados com base nos critérios e filtros fornecidos
    const values = selectElementFilter(data.data.args, data.data.filter);

    // Envia os dados extraídos de volta ao backend para manipulação posterior
    window.pywebview.api.read_callback({ data: values });
}

/**
 * Filtra propriedades específicas de um elemento DOM.
 *
 * @param {HTMLElement} element - Elemento HTML a ser processado.
 * @param {Array<string>} filter - Lista de propriedades a serem extraídas.
 * @returns {Array<any>} - Valores extraídos com base no filtro, na ordem fornecida.
 */
function filterValuesFromElement(element, filter) {
    const map = {
        value: el => el.value ?? null,               // Valor de inputs, selects etc.
        text: el => el.innerText,                    // Texto visível
        html: el => el.innerHTML,                    // Conteúdo HTML interno
        style: el => el.getAttribute('style') ?? ''  // Estilo inline
    };

    // Mapeia as chaves do filtro para os valores extraídos do elemento
    return filter.map(key => map[key]?.(element) ?? null);
}







/**
 * Seleciona múltiplos elementos com base em seletores fornecidos,
 * aplica um filtro de propriedades desejadas e retorna os valores extraídos.
 *
 * @param {Array<string>} args - Lista de seletores CSS a serem utilizados.
 * @param {Array<string>} filter - Lista de propriedades a serem extraídas de cada elemento.
 * @returns {Array<any>} - Lista com os valores filtrados de cada elemento encontrado.
 */
function selectElementFilter(args, filter) {
    const data = [];

    args.forEach(arg => {
        // Seleciona todos os elementos que correspondem ao seletor atual
        const query = document.querySelectorAll(arg);

        if (query && query.length > 0) {
            // Para cada elemento encontrado, aplica o filtro e adiciona ao array de saída
            query.forEach(element => {
                data.push(filterValuesFromElement(element, filter));
            });
        } else {
            // Se nenhum elemento for encontrado para o seletor, exibe mensagem no console Python
            msg('Nenhum elemento foi selecionado em:', arg);
        }
    });

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

"""

    html = f"""
<!DOCTYPE html>
<html lang="{lang}">
<head>
   
    <script class="main-reserve">{script}</script>
</head>
<body>
</body>
</html>"""
    create_folder()
    create_file(f'static/index.html', html)  # Grava o conteúdo no caminho especificado