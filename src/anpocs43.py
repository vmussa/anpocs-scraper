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
    insider = is_inside_div(tag)
    return (
        is_child_of_span and is_strong and not excluded and insider
    )

def is_title(tags):
    titles = tags[1::2]
    return titles

def is_session(tags):
    sessions = tags[::2]
    return sessions

def is_author(tag):
    pass

def is_abstract(tag):
    pass

def get_titles_and_session_tags():
    tags = soup.find_all(is_title_or_session)
    return tags

def get_tags_texts(tags):
    texts = [tag.text for tag in tags]
    return texts

def get_titles():
    tags = get_titles_and_session_tags()
    titles_tags = is_title(tags)
    titles = [title.text for title in titles_tags]
    return titles

def get_sessions():
    tags = get_titles_and_session_tags()
    sessions_tags = is_session(tags)
    sessions = [session.text for session in sessions_tags]
    return sessions

def get_authors():
    authors_tags = soup.find_all(is_author)
    authors = [author.text for author in authors_tags]
    return authors

def get_abstracts_tags():
    tags = soup.find_all(is_abstract)
    return tags

def get_abstracts(tags):
    # abstracts = is_abstract(tags)
    # return abstracts
    pass

def main():
    titles = get_titles()
    sessions = get_sessions()
    #abstracts = get_abstracts()
    #authors = get_authors()

    data = {
        'autores': None,
        'titulo': titles,
        'resumo': None,
        'sessao': sessions,
        'id_evento': EVENT_ID
    }

    df = pd.DataFrame(data)
    df.to_csv('resumos_anpocs43.csv', index=False)
    import ipdb; ipdb.set_trace()

if __name__ == "__main__":
    main()
