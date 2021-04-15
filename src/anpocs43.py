"""Código para a raspagem dos resumos 43º Encontro Anual da ANPOCS."""
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
    exclusions = ["não", "Palavras-chave:", "ETHOS"]
    exclude = lambda x: x in exclusions
    insider = is_inside_div(tag)
    return (
        is_child_of_span and is_strong and not exclude(tag.text) and insider
    )

def is_title(tags):
    titles = tags[1::2]
    return titles

def is_session(tags):
    sessions = tags[::2]
    return sessions

def is_author(tag):
    is_span = tag.name == 'span'
    has_strong = tag.find('strong')
    if has_strong:
        has_session_info = has_strong.find(string=re.compile(r'ST\d\d|SPG\d\d'))
    is_inside = is_inside_div(tag)
    return is_span and has_strong and is_inside and has_session_info

def is_abstract(tag):
    is_span = tag.name == 'span'
    has_not_strong = not tag.find('strong')
    has_key_word = tag.find('strong', string='Palavras-chave:')
    is_inside = is_inside_div(tag)
    return is_inside and is_span and (has_not_strong or has_key_word)
    
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

def get_abstracts():
    tags = get_abstracts_tags()
    abstracts = [abstract.text for abstract in tags]
    return abstracts

def clean_data(df):
    df.loc[477, 'resumo'] += df.loc[478, 'resumo'] + df.loc[479, 'resumo']
    df.drop([0, 1, 79, 80, 301, 478, 479, 573, 619, 620, 621], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def main():
    print("Começando a raspagem do 43º Encontro Anual da ANPOCS...")
    titles = get_titles()
    sessions = get_sessions()
    abstracts = get_abstracts()
    authors = get_authors()

    data = {
        'autores': authors,
        'titulo': titles,
        'sessao': sessions,
        'id_evento': EVENT_ID
    }

    df_abstracts = pd.DataFrame(abstracts, columns=['resumo'])
    df_abstracts = clean_data(df_abstracts)
    df = pd.DataFrame(data)
    df = pd.concat([df, df_abstracts], axis=1)
    df.to_csv('resumos_anpocs43.csv', index=False)
    print("O 43º Encontro foi raspado com sucesso.")
    import ipdb; ipdb.set_trace()

if __name__ == "__main__":
    main()
