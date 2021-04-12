"""Código para a raspagem dos resumos 43º Encontro Anual da ANPOCS."""
import requests
from bs4 import BeautifulSoup
import pandas as pd

EVENT_ID = 43
URL = ("http://anpocs.com/index.php/43-encontro-anual-2019/2750-encontros-anu"
       "ais/43-encontro/2301-resumos-sts-e-spgs")

r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html.parser')

def is_inside_div(tag):
    for parent in tag.parents:
        try:
            if "rt-article-bg" in parent['class']:
                return True
        except KeyError:
            pass
    return False

def is_title_or_session(tag):
    is_child_of_span = tag.parent.name == 'span'
    is_strong = tag.name == 'strong'
    excluded = tag.text == "Palavras-chave:"
    return is_child_of_span and is_strong and not excluded

def get_tags_texts(tags):
    texts = [tag.text for tag in tags]
    return texts

def get_titles(tags):
    titles = tags[1::2]
    return titles

def get_sessions(tags):
    sessions = tags[::2]
    return sessions

def main():
    tags_found = soup.find_all(is_title_or_session)
    tags = [tag for tag in tags_found if is_inside_div(tag)]
    tags_texts = get_tags_texts(tags)

    titles = get_titles(tags_texts)
    sessions = get_sessions(tags_texts)

    data = {
        'autores': None,
        'titulo': titles,
        'resumo': None,
        'sessao': sessions,
        'id_evento': EVENT_ID
    }

    df = pd.DataFrame(data)
    df.to_csv('resumos_anpocs43.csv', index=False)

if __name__ == "__main__":
    main()
