import re
from datetime import date
from requests import get
from bs4 import BeautifulSoup

def web_scrap(produto_buscado):
    ''' Faz o web scrap no sit do olx e retorna uma lista de
    dicionários com os itens encontrados. '''

    url = 'https://sp.olx.com.br/grande-campinas?q={}'.format(produto_buscado)

    # Regex que remove os \n, \r e \t dos textos
    regex = re.compile('[\n\r\t]')

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0"}
    request = get(url, headers=headers)

    soup = BeautifulSoup(request.text, 'html.parser')

    lista_resultados = soup.find('ul', id='ad-list')
    itens = lista_resultados.find_all('li')

    itens_encontrados = []

    for item in itens:
        if item.has_attr('data-list_id'):
            link = item.find('a')

            # Titulo do produto
            obj_titulo = link.find('h2', class_='OLXad-list-title')
            titulo = regex.sub('', obj_titulo.text)

            # Preço do produto
            obj_preco = link.find('p', class_='OLXad-list-price')
            if not obj_preco: # Não pegar produtos sem preços
                continue
            # Pegar o preço, removendo o cifrão e o ponto
            preco = regex.sub('', obj_preco.text.replace('R$', '')).replace('.','').strip()

            # Local do vendedor
            obj_local = link.find('p', class_='text detail-region')
            local = regex.sub('', obj_local.text)

            # Link do anúncio
            link_produto = link['href']

            itens_encontrados.append({
                'titulo' : titulo,
                'preco' : preco,
                'local' : local,
                'link' : link_produto,
                'data_pesquisa' : date.today()
            })

    return itens_encontrados
