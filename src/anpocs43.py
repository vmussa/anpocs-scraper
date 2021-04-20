"""Código para a raspagem dos resumos 43º Encontro Anual da ANPOCS."""
from os import mkdir, sep
from os.path import abspath, dirname, exists
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

EVENT_ID = 43
URL = ("http://anpocs.com/index.php/43-encontro-anual-2019/2750-encontros-anu"
       "ais/43-encontro/2301-resumos-sts-e-spgs")

r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html.parser')

def is_inside_div(tag):
    """Retorna True se a tag estiver dentro do div principal.
    Retorna False para o caso contrário."""
    for parent in tag.parents:
        try:
            if "rt-article-bg" in parent['class']:
                return True
        except KeyError:
            pass
    return False

def is_title_or_session(tag):
    """Retorna True para as tags referentes a títulos ou sessões.
    Retorna False para o caso contrário."""
    is_child_of_span = tag.parent.name == 'span'
    is_strong = tag.name == 'strong'
    exclusions = ["não", "Palavras-chave:", "ETHOS"]
    exclude = lambda x: x in exclusions
    insider = is_inside_div(tag)
    return (
        is_child_of_span and is_strong and not exclude(tag.text) and insider
    )

def is_title(tags):
    """Retorna a lista de tags referentes a títulos."""
    titles = tags[1::2]
    return titles

def is_session(tags):
    """Retorna a lista de tags referentes a sessões."""
    sessions = tags[::2]
    return sessions

def is_author(tag):
    """Retorna True para as tags referentes a autores.
    Retorna False para o caso contrário."""
    is_span = tag.name == 'span'
    has_strong = tag.find('strong')
    if has_strong:
        has_session_info = has_strong.find(string=re.compile(r'ST\d\d|SPG\d\d'))
    is_inside = is_inside_div(tag)
    return is_span and has_strong and is_inside and has_session_info

def is_abstract(tag):
    """Retorna True para as tags referentes a resumos.
    Retorna False para o caso contrário."""
    is_span = tag.name == 'span'
    has_not_strong = not tag.find('strong')
    has_key_word = tag.find('strong', string='Palavras-chave:')
    is_inside = is_inside_div(tag)
    return is_inside and is_span and (has_not_strong or has_key_word)
    
def get_titles_and_session_tags():
    """Retorna uma lista de tags referentes aos títulos e sessões."""
    tags = soup.find_all(is_title_or_session)
    return tags

def get_tags_texts(tags):
    """Retorna uma lista com o conteúdo textual das tags."""
    texts = [tag.text for tag in tags]
    return texts

def get_titles():
    """Retorna uma lista de títulos."""
    tags = get_titles_and_session_tags()
    titles_tags = is_title(tags)
    titles = [title.text for title in titles_tags]
    return titles

def get_sessions():
    """Retorna uma lista de sessões."""
    tags = get_titles_and_session_tags()
    sessions_tags = is_session(tags)
    sessions = [session.text for session in sessions_tags]
    return sessions

def get_authors():
    """Retorna uma lista de autores."""
    authors_tags = soup.find_all(is_author)
    authors = [author.text for author in authors_tags]
    return authors

def get_abstracts_tags():
    """Retorna uma lista de tags referentes a resumos."""
    tags = soup.find_all(is_abstract)
    return tags

def get_abstracts():
    """Retorna uma lista de resumos."""
    tags = get_abstracts_tags()
    raw_abstracts = [abstract.text for abstract in tags]
    abstracts = clean_abstracts(raw_abstracts)
    return abstracts

def clean_abstracts(raw_abstracts):
    """Limpa a lista de resumos."""
    df = pd.DataFrame(raw_abstracts, columns=['resumo'])
    df.loc[476, 'resumo'] += df.loc[477, 'resumo'] + df.loc[478, 'resumo']
    df.drop([0, 1, 79, 301, 477, 478, 573, 619, 620, 621], inplace=True)
    df.reset_index(drop=True, inplace=True)
    abstracts = df.to_dict(orient='list')['resumo']
    return abstracts

def main():
    print("Começando a raspagem do 43º Encontro Anual da ANPOCS...")
    authors = get_authors()
    titles = get_titles()
    abstracts = get_abstracts()
    sessions = get_sessions()

    data = {
        'autores': authors,
        'titulo': titles,
        'resumo': abstracts,
        'sessao': sessions,
        'id_evento': EVENT_ID
    }
    
    df = pd.DataFrame(data)

    # gera o CSV com os resultados da raspagem
    output_path = f"{dirname(dirname(abspath(__file__)))}{sep}output{sep}"
    filename = "resumos_anpocs43.csv"
    if exists(output_path):
        df.to_csv(output_path + filename, index=False)
    else:
        mkdir(output_path)
        df.to_csv(output_path + filename, index=False)

    print("O 43º Encontro foi raspado com sucesso.")

if __name__ == "__main__":
    main()
