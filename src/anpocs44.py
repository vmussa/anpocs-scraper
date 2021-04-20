"""Código para a aquisição dos dados dos Encontros Anuais da ANPOCS."""
from bs4 import BeautifulSoup
import pandas as pd
import re
from tqdm import tqdm
import sys
from os import mkdir, sep
from os.path import abspath, dirname, exists
import requests
from helium import (
    start_chrome, click, get_driver, kill_browser, find_all, S
)

EVENT_ID = 44
BASE_URLS = [
    "https://www.anpocs2020.sinteseeventos.com.br/atividade/hub/gt",
    "https://www.anpocs2020.sinteseeventos.com.br/atividade/hub/simposioposgraduada"
]

def get_page_source(url):
    """Obtém soup object para páginas não interativas."""
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def get_urls(base_urls):
    """Obtém todos os URLs das páginas a serem raspadas."""
    urls = []
    for base_url in base_urls:
        soup = get_page_source(base_url)
        urls_sources = soup.select("h5 > a")
        urls += [a['href'] for a in urls_sources]
    return urls

def get_interactive_page_source(url):
    """Obtém código-fonte completo da página."""
    # inicia o chrome para renderizar o código-fonte 
    try:
        start_chrome(url, headless=True)
    except Exception:
        print(
            "Erro: você precisa instalar o Google Chrome e o ChromeDriver par"
            "a executar esse raspador."
            )
        sys.exit(1)
    
    driver = get_driver()

    # clica em todos os botões "Veja mais!" para liberar os dados dos resumos
    print(f"Raspando a página \"{driver.title}\". Isso pode demorar alguns segundos...")
    buttons = find_all(S("//span[@onClick]"))
    for _ in tqdm(range(len(buttons))):
        click("Veja mais!")
    print('Fim da raspagem da página.')

    # obtém objeto soup a partir do código-fonte renderizado pelo helium
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # fecha o chrome
    kill_browser()

    return soup

def get_page_data(soup):
    """Obtém dados dos trabalhos apresentados em uma sessão."""
    # obtém dados textuais a partir dos seletores CSS de cada campo 
    authors = [autor.text for autor in soup.select('i')]
    titles = [titulo.text for titulo in soup.select('li > b')]
    abstract_source = soup.find_all('div', id=re.compile('^resumoFull'))
    abstracts = [abstract.text.strip() for abstract in abstract_source]
    session = soup.select_one('h3.first').text.strip()

    # cria dict com os dados obtidos
    data = {
        'autores': authors,
        'titulo': titles,
        'resumo': abstracts,
        'sessao': session,
        'id_evento': EVENT_ID
    }

    return data

def export_all_pages_data(urls):
    """Obtém e exporta para CSV dados de trabalhos de todas as sessões."""
    for url in urls:
        soup = get_interactive_page_source(url)
        data = get_page_data(soup)
        df = pd.DataFrame(data)

        output_path = f"{dirname(dirname(abspath(__file__)))}{sep}output{sep}"
        filename = "resumos_anpocs44.csv"        
        if exists(output_path+filename):
            df.to_csv(
                output_path + filename,
                mode='a',
                index=False,
                header=False
                )
        else:
            try:
                mkdir(output_path)
                df.to_csv(output_path + filename, index=False)
            except FileExistsError:
                df.to_csv(output_path + filename, index=False)

def main():
    print(
        "Carregando algumas informações. A raspagem do 44º Encontro Anual da "
        "ANPOCS iniciará em breve..."
    )
    urls = get_urls(BASE_URLS)
    export_all_pages_data(urls)
    print("O 44º Encontro foi raspado com sucesso.")

if __name__ == "__main__":
    main()
