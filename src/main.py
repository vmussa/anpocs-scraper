"""Código para a aquisição dos dados dos Encontros Anuais da ANPOCS."""
from bs4 import BeautifulSoup
import pandas as pd
import re
from tqdm import tqdm
import requests
from helium import (
    start_chrome, click, get_driver, kill_browser, find_all, S
)

BASE_URL = "https://www.anpocs2020.sinteseeventos.com.br/atividade/hub/gt"

def get_page_source(url):
    """Obtém soup object para páginas não interativas."""
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def get_urls(base_url):
    soup = get_page_source(BASE_URL)
    urls_sources = soup.select("h5 > a")
    urls = [a['href'] for a in urls_sources]
    return urls

def get_interactive_page_source(url):
    """Obtém código-fonte completo da página."""
    # inicia o chrome para renderizar o código-fonte 
    start_chrome(url, headless=True)

    # clica em todos os botões "Veja mais!" para liberar os dados dos resumos
    print("Clicando em todos os botões. Isso pode demorar alguns segundos...")
    buttons = find_all(S("//span[@onClick]"))
    for i in tqdm(range(len(buttons))):
        click("Veja mais!")
        print(f"\nClique número {i}: um resumo aberto...")
    print('Fim dos cliques. Todos os resumos estão disponíveis.')

    # obtém objeto soup a partir do código-fonte renderizado pelo helium
    driver = get_driver()
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

    # cria dict com os dados obtidos
    data = {
        'autores': authors,
        'titulo': titles,
        'resumo': abstracts
    }

    return data

def get_all_pages_data(urls):
    """Obtém dados de trabalhos de todas as sessões."""
    for _, url in enumerate(urls):
        soup = get_interactive_page_source(url)
        data = get_page_data(soup)
        df = pd.DataFrame(data)
        df.to_csv(f'{_}anpocs_publications.csv', index=False)

if __name__ == "__main__":
    urls = get_urls(BASE_URL)
    get_all_pages_data(urls)
