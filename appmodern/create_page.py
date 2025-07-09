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
 * Classe responsável pela criação dinâmica de elementos HTML, com atributos,
 * filhos e inserção automática no DOM.
 */
class CreateElement {
    /**
     * Construtor da classe CreateElement.
     * 
     * @param {HTMLElement|string} parent - Elemento pai ou seletor CSS onde o novo elemento será inserido.
     * @param {string} element - Tipo da tag HTML a ser criada (ex: 'div', 'span').
     * @param {Object} attributes - Objeto contendo os atributos HTML do elemento.
     * @param {Array} childrens - Lista de filhos (elementos ou textos) a serem inseridos.
     * @param {boolean} insert - Define se o novo elemento será automaticamente inserido no DOM.
     */
    constructor(parent, element, attributes, childrens, insert = true) {
        this.parent = (typeof parent === 'string') ? document.querySelector(parent) : parent;
        this.element = document.createElement(element);
        this.set_attribute(attributes);
        this.create_childrens(childrens);
        if (insert) {
            this.insert_element();
        }
    }

    /**
     * Cria e adiciona um filho ao elemento principal.
     * Aceita um objeto com especificação de elemento dinâmico
     * ou um valor simples (string/número) como texto.
     * 
     * @param {Object|string|number} element - Elemento filho ou texto simples.
     */
    create_children(element) {
        try {
            const dinamic_element = new CreateElement(
                this.element,
                element.element,
                element.attributes,
                element.childrens
            );
            components.add_components(dinamic_element.element);
        } catch (error) {
            if (typeof element === 'string' || typeof element === 'number') {
                this.element.innerText += element;
            }
        }
    }

    /**
     * Itera sobre os filhos declarados e os adiciona ao elemento.
     * 
     * @param {Array} childrens - Lista de filhos a serem processados.
     */
    create_childrens(childrens) {
        childrens.forEach(child => this.create_children(child));
    }

    /**
     * Define os atributos HTML fornecidos no elemento.
     * 
     * @param {Object} attributes - Objeto contendo os atributos no formato chave/valor.
     */
    set_attribute(attributes) {
        if (attributes) {
            for (const [key, value] of Object.entries(attributes)) {
                this.element.setAttribute(key, value);
            }
        }
    }

    /**
     * Insere o elemento criado como filho do elemento pai no DOM.
     */
    insert_element() {
        this.parent.appendChild(this.element);
    }
}

/**
 * Classe responsável por organizar e classificar elementos HTML de forma estruturada,
 * utilizando sua tag e atributos relevantes como chaves de agrupamento.
 */
class Components {
    /**
     * Inicializa a estrutura de armazenamento dos componentes categorizados por tag.
     */
    constructor() {
        /**
         * Objeto de armazenamento onde cada chave é uma tag HTML e os valores são
         * arrays de elementos classificados por tipo de atributo (id, name, class, genérico).
         * 
         * Exemplo:
         * {
         *   div: { id: [...], name: [...], class: [...], generic: [...] },
         *   input: { ... },
         * }
         */
        this.components = {};
    }

    /**
     * Adiciona um elemento HTML à estrutura de componentes, classificando-o com base
     * nos seus atributos (id, name, class ou outros).
     *
     * @param {HTMLElement} element - Elemento DOM a ser inserido e classificado.
     */
    add_components(element) {
        // Normaliza o nome da tag para letras minúsculas, garantindo consistência nas chaves
        const tag = element.tagName.toLowerCase();

        // Inicializa o agrupamento da tag caso ainda não exista
        if (!(tag in this.components)) {
            this.components[tag] = {
                id: [],
                name: [],
                class: [],
                generic: [],
            };
        }

        // Classifica o elemento conforme os atributos presentes
        if (element.id) {
            this.components[tag].id.push(element);
        } else if (element.getAttribute('name')) {
            this.components[tag].name.push(element);
        } else if (element.className && element.className.trim() !== '') {
            this.components[tag].class.push(element);
        } else {
            this.components[tag].generic.push(element);
        }
    }
}

/**
 * Classe responsável por buscar e filtrar elementos DOM dinamicamente,
 * com base em atributos estruturais como tag, id, name e class.
 */
class Search {
    /**
     * Inicializa os atributos internos da busca, incluindo o elemento alvo,
     * os resultados da filtragem e um mapa descritivo dos critérios aplicados.
     */
    constructor() {
        this.element = null;
        this.result = {};
        this.map = {
            'tag': null,
            'group': null,
            'elements': null,
        };
    }

    /**
     * Filtra os resultados buscando elementos com o mesmo ID do elemento alvo.
     */
    get_id() {
        this.result = this.result.filter(element => element.id === this.element.id);
    }

    /**
     * Filtra os resultados buscando elementos com o mesmo atributo 'name'.
     */
    get_name() {
        this.result = this.result.filter(
            element => element.getAttribute('name') === this.element.getAttribute('name')
        );
    }

    /**
     * Filtra os resultados buscando elementos com a mesma classe CSS.
     */
    get_class() {
        this.result = this.result.filter(
            element => element.className === this.element.className
        );
    }

    /**
     * Aplica o filtro baseado nos atributos prioritários:
     * ID > name > class > genérico. Define o agrupamento correspondente.
     */
    attributes_filter() {
        if (this.element.id) {
            this.result = this.result.id;
            this.map.group = 'id';
            this.get_id();
        } else if (this.element.getAttribute('name')) {
            this.result = this.result.name;
            this.map.group = 'name';
            this.get_name();
        } else if (this.element.className && this.element.className.trim() !== '') {
            this.result = this.result.class;
            this.map.group = 'class';
            this.get_class();
        } else {
            this.map.group = 'generic';
            this.result = this.result.generic;
        }
    }

    /**
     * Verifica se a tag do elemento existe nos componentes registrados.
     * Caso positivo, atualiza o mapa e define o conjunto inicial de busca.
     *
     * @returns {boolean} - Verdadeiro se a tag foi localizada nos componentes.
     */
    tag_filter() {
        const tag = this.element.tagName.toLowerCase();
        if (tag in components.components) {
            this.result = components.components[tag];
            this.map.tag = tag;
            return true;
        }
        return false;
    }

    /**
     * Cria uma instância dinâmica do elemento baseado nas propriedades fornecidas.
     * Este elemento será usado como base para filtragem posterior.
     *
     * @param {Object} element - Objeto contendo dados para construção do elemento DOM.
     */
    create_element(element) {
        const dinamic_element = new CreateElement(
            element.parent,
            element.element,
            element.attributes,
            element.childrens,
            false
        );
        this.element = dinamic_element.element;
    }

    /**
     * Restaura o estado interno da instância, limpando o elemento e os resultados prévios.
     */
    reset() {
        this.element = null;
        this.result = {};
    }

    /**
     * Executa o ciclo completo de busca:
     * - Cria o elemento dinâmico
     * - Aplica filtro por tag
     * - Aplica filtro por atributos
     * - Retorna o mapa estruturado com informações da busca.
     *
     * @param {Object} element - Dados do elemento a ser buscado.
     * @returns {Object} - Mapa contendo tag, tipo de agrupamento e elementos encontrados.
     */
    get(element) {
        this.reset();
        this.map = {
            'tag': null,
            'group': null,
            'elements': null,
        };
        this.create_element(element);
        this.tag_filter();
        this.attributes_filter();
        this.map.elements = this.result;
        return this.map;
    }
}

class UpdateElement {


    clone(before, after){
        // Copia atributos
        for (let attr of after.attributes) {
        before.setAttribute(attr.name, attr.value);

        // Se for input e o atributo for 'value', atualiza também a propriedade real
        if (attr.name === 'value' && (before.tagName === 'INPUT' || before.tagName === 'TEXTAREA')) {
            before.value = attr.value;
        }
    }


        // Copia estilos computados
        const style_new = window.getComputedStyle(after);
        for (let prop of style_new) {
            before.style[prop] = style_new.getPropertyValue(prop);
        }

        before.innerHTML = '';
        before.innerHTML = after.innerHTML;



    }

    update(elements, after){
        elements.forEach(before => {
            this.clone(before, after);
        });
    }

    get(before, after){
       var map = search.get(before);
       let dinamic_element = new CreateElement(
                after.parent,
                after.element,
                after.attributes,
                after.childrens,
                false,
            );
        let element_after = dinamic_element.element;
        this.update(map.elements, element_after);

        
    }
}

// INSTANCIAS NECESSARIAS
const components = new Components();
const search = new Search();
const update_element = new UpdateElement();

// FUNÇÕES NECESSARIAS

/**
 * Lê elementos do DOM com base nos dados recebidos do backend,
 * filtra e envia o resultado de volta para o Python.
 */
async function read() {
    // Solicita ao backend os critérios de busca para os elementos
    const data = await window.pywebview.api.get_data();
    const get_data = [];

    // Itera sobre os critérios recebidos e procura os elementos correspondentes no DOM
    data.data.forEach(element => {
        const map = search.get(element);
        if (map && Array.isArray(map.elements)) {
            map.elements.forEach(element_map => {

                // Coleta os dados relevantes do elemento DOM
                get_data.push({
                    element: element_map.tagName || null,
                    value: element_map.value ?? null,
                    text: element_map.innerText ?? null,
                    html: element_map.innerHTML ?? null,
                    id: element_map.id ?? null,
                    class: element_map.className ?? null,
                    name: (typeof element_map.getAttribute === 'function')
                        ? element_map.getAttribute('name')
                        : null
                });
            });
        }
    });

    // Envia os dados extraídos de volta ao Python para manipulação posterior
    window.pywebview.api.read_callback({ data: get_data });
}

/**
 * Remove elementos do DOM com base nos dados recebidos do backend.
 * Atualiza o armazenamento local dos componentes após a exclusão.
 */
async function del() {
    let data = await window.pywebview.api.get_data();
    if (data) {
        data.data.forEach(element => {
            //Filtra os elementos
            const map = search.get(element);

            // Remove cada elemento DOM encontrado
            map.elements.forEach(el => el.remove());

            // Atualiza a lista de componentes no agrupamento correspondente
            const old_list = components.components[map.tag][map.group];
            const new_list = old_list.filter(item => !map.elements.includes(item));
            components.components[map.tag][map.group] = new_list;

        });
    }
}

async function update() {
    let data = await window.pywebview.api.get_data();
    if (data) {
        data.data.forEach(element => {
            update_element.get(element.before, element.after);
        });
    }
}

/**
 * Cria e insere dinamicamente elementos HTML com base nos dados recebidos do Python.
 * Os elementos são registrados na estrutura de componentes local.
 */
async function create() {
    let data = await window.pywebview.api.get_data();
    if (data) {
        
        data.data.forEach(element => {
            const dinamic_element = new CreateElement(
                element.parent,
                element.element,
                element.attributes,
                element.childrens
            );
            components.add_components(dinamic_element.element);
        });
    }
}

/**
 * Cria dinamicamente os elementos da seção <head> da página,
 * utilizando os dados iniciais enviados pelo backend Python.
 */
async function loading_head() {
    let data = await window.pywebview.api.get_data();
    if (data) {
        data.data[0].childrens.forEach(element => {
            const dinamic_element = new CreateElement(
                window.document.head,
                element.element,
                element.attributes,
                element.childrens
            );
            components.add_components(dinamic_element.element);
        });
    }
}

/**
 * Executa uma rota registrada via PyWebView, disparando a função Python correspondente.
 *
 * @param {string} function_route - Nome da rota a ser acionada no backend.
 */
function call(function_route) {
    window.pywebview.api.route_exec(function_route);
}

/**
 * Evento disparado quando o PyWebView termina de carregar.
 * Inicia o carregamento da seção <head> via API Python.
 */
window.addEventListener('pywebviewready', function () {
    console.log('A API do PyWebView está pronta!');
    window.pywebview.api.loading();
});"""
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